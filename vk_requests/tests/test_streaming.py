# -*- coding: utf-8 -*-
import os
import sys
import pytest
import asyncio
from vk_requests.streaming import StreamingAPI

SERVICE_TOKEN = os.getenv('VK_SERVICE_TOKEN')


@pytest.fixture
def api():
    return StreamingAPI(service_token=SERVICE_TOKEN)


@pytest.mark.skipIf(sys.version_info < (3, 4), reason="py34+")
def test_streaming_api_basics(api):
    # api.remove_rule(tag='hello')
    resp = api.add_rule(value='Hello', tag='test_hello')
    assert resp['code'] == 200

    # Catch double add
    resp = api.add_rule(value='Hello', tag='test_hello')
    assert resp['code'] == 400
    assert resp['error']['message'] == 'Tag already exist'

    settings = api.get_settings()
    assert 'monthly_limit' in settings

    rules = api.get_rules()
    assert rules == {
        'rules': [{'value': 'Hello', 'tag': 'test_hello'}], 'code': 200}

    resp = api.remove_rule(tag='test_hello')
    assert resp['code'] == 200


@pytest.mark.skipIf(sys.version_info < (3, 4), reason="py34+")
def test_stream_consumer(api):
    # Add test rule to consume messages
    api.add_rule(value='Привет', tag='test_hello')
    stream = api.get_stream()
    handler_was_called = None

    @stream.consumer
    @asyncio.coroutine
    def handle_event(payload):
        global handler_was_called
        handler_was_called = True
        print(payload)

    stream.consume(timeout=10)
    api.remove_rule(tag='test_hello')
    # assert handler_was_called is True
