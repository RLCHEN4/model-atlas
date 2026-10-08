import importlib.util
import unittest
from pathlib import Path
from urllib.error import HTTPError, URLError
spec = importlib.util.spec_from_file_location('check_sources', Path(__file__).resolve().parents[1] / 'scripts' / 'check_sources.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
class FakeResponse:
    def __init__(self, status=200):
        self.status = status
    def __enter__(self):
        return self
    def __exit__(self, *args):
        return False
class LinkChecks(unittest.TestCase):
    def test_available(self):
        self.assertTrue(module.check('test', 'https://example.com', lambda req, timeout: FakeResponse(200))['ok'])
    def test_unavailable(self):
        self.assertFalse(module.check('test', 'https://example.com', lambda req, timeout: FakeResponse(503))['ok'])
    def test_network_error(self):
        def broken(req, timeout):
            raise URLError('offline')
        self.assertFalse(module.check('test', 'https://example.com', broken)['ok'])
    def test_fallback_get_if_head_unsupported(self):
        methods = []
        def fallback(req, timeout):
            methods.append(req.get_method())
            if req.get_method() == 'HEAD':
                raise HTTPError(req.full_url, 405, 'unsupported', None, None)
            return FakeResponse(204)
        self.assertTrue(module.check('test', 'https://example.com', fallback)['ok'])
        self.assertEqual(methods, ['HEAD', 'GET'])
    def test_does_not_export_benchmark_fields(self):
        self.assertEqual(set(module.check('test', 'https://example.com', lambda req, timeout: FakeResponse()).keys()), {'name', 'ok'})
if __name__ == '__main__':
    unittest.main()
