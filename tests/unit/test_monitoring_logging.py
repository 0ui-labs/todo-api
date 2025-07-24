"""Unit tests for structured logging configuration."""
import json
import logging
from io import StringIO
from unittest.mock import patch

import pytest

from app.monitoring.logging_config import (
    ContextFilter,
    CustomJsonFormatter,
    request_id_context,
    user_id_context,
    trace_id_context,
    span_id_context,
    setup_logging,
    get_logger,
)


class TestContextFilter:
    """Test context filter for logging."""
    
    def test_context_filter_adds_attributes(self):
        """Test that context filter adds context variables to log record."""
        # Set context variables
        request_id_context.set("test-request-123")
        user_id_context.set("user-456")
        trace_id_context.set("trace-789")
        span_id_context.set("span-abc")
        
        # Create filter and log record
        filter_instance = ContextFilter()
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="test.py",
            lineno=1,
            msg="Test message",
            args=(),
            exc_info=None
        )
        
        # Apply filter
        filter_instance.filter(record)
        
        # Check attributes added
        assert record.request_id == "test-request-123"
        assert record.user_id == "user-456"
        assert record.trace_id == "trace-789"
        assert record.span_id == "span-abc"
        
        # Clean up
        request_id_context.set(None)
        user_id_context.set(None)
        trace_id_context.set(None)
        span_id_context.set(None)
    
    def test_context_filter_handles_none(self):
        """Test context filter handles None values."""
        # Ensure context is clear
        request_id_context.set(None)
        user_id_context.set(None)
        
        # Create filter and log record
        filter_instance = ContextFilter()
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="test.py",
            lineno=1,
            msg="Test message",
            args=(),
            exc_info=None
        )
        
        # Apply filter
        filter_instance.filter(record)
        
        # Check attributes are None
        assert record.request_id is None
        assert record.user_id is None


class TestCustomJsonFormatter:
    """Test custom JSON formatter."""
    
    def test_json_formatter_output(self):
        """Test JSON formatter produces valid JSON with expected fields."""
        formatter = CustomJsonFormatter(
            "%(timestamp)s %(severity)s %(name)s %(message)s"
        )
        
        # Create log record
        record = logging.LogRecord(
            name="test.logger",
            level=logging.INFO,
            pathname="/app/test.py",
            lineno=42,
            msg="Test log message",
            args=(),
            exc_info=None
        )
        
        # Add context attributes
        record.request_id = "req-123"
        record.user_id = "user-456"
        
        # Format record
        formatted = formatter.format(record)
        
        # Parse JSON
        log_data = json.loads(formatted)
        
        # Check required fields
        assert log_data["message"] == "Test log message"
        assert log_data["severity"] == "INFO"
        assert log_data["logger"] == "test.logger"
        assert "timestamp" in log_data
        assert "source" in log_data
        
        # Check source fields
        assert log_data["source"]["file"] == "/app/test.py"
        assert log_data["source"]["line"] == 42
        assert log_data["source"]["function"] == "<module>"
        
        # Check context fields
        assert log_data["request_id"] == "req-123"
        assert log_data["user_id"] == "user-456"
    
    def test_json_formatter_exception(self):
        """Test JSON formatter handles exceptions."""
        formatter = CustomJsonFormatter("%(message)s")
        
        # Create log record with exception
        try:
            raise ValueError("Test error")
        except ValueError:
            import sys
            exc_info = sys.exc_info()
        
        record = logging.LogRecord(
            name="test",
            level=logging.ERROR,
            pathname="test.py",
            lineno=1,
            msg="Error occurred",
            args=(),
            exc_info=exc_info
        )
        
        # Format record
        formatted = formatter.format(record)
        log_data = json.loads(formatted)
        
        # Check exception included
        assert "exception" in log_data
        assert "ValueError: Test error" in log_data["exception"]


class TestLoggingSetup:
    """Test logging setup function."""
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_setup_logging_json_mode(self, mock_stdout):
        """Test logging setup in JSON mode."""
        # Setup logging
        setup_logging(
            level="INFO",
            json_logs=True,
            service_name="test-service"
        )
        
        # Get logger and log a message
        logger = get_logger("test")
        logger.info("Test message", extra={"custom_field": "value"})
        
        # Get output
        output = mock_stdout.getvalue()
        
        # Parse JSON
        log_data = json.loads(output.strip())
        
        # Check fields
        assert log_data["message"] == "Test message"
        assert log_data["severity"] == "INFO"
        assert log_data["logger"] == "test"
        assert log_data["custom_field"] == "value"
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_setup_logging_text_mode(self, mock_stdout):
        """Test logging setup in text mode."""
        # Setup logging
        setup_logging(
            level="DEBUG",
            json_logs=False,
            service_name="test-service"
        )
        
        # Set context
        request_id_context.set("req-789")
        
        # Get logger and log a message
        logger = get_logger("test")
        logger.debug("Debug message")
        
        # Get output
        output = mock_stdout.getvalue()
        
        # Check text format
        assert "DEBUG" in output
        assert "[req-789]" in output
        assert "Debug message" in output
        
        # Clean up
        request_id_context.set(None)
    
    def test_get_logger(self):
        """Test get_logger returns correct logger."""
        logger = get_logger("test.module")
        assert logger.name == "test.module"
        assert isinstance(logger, logging.Logger)