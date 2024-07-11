import unittest
from unittest.mock import MagicMock
from nodes.fw_nodes import CountTokens, TrimToTokens, TokenCountRanker, FileCountInDirectory

class TestFearnworksNodes(unittest.TestCase):

    def setUp(self):
        self.mock_clip = MagicMock()
        # Simulate CLIP tokenizer behavior more accurately
        self.mock_clip.tokenize.return_value = {'g': [["49406", "1", "2", "3", "49407"]]}
        # Simulate CLIP encode_from_tokens behavior
        self.mock_clip.encode_from_tokens.return_value = (MagicMock(), MagicMock())

    def test_token_count_ranker(self):
        token_count_ranker = TokenCountRanker()
        result = token_count_ranker.sort_segments_and_words_by_token_count(self.mock_clip, "Test, text")
        self.assertIn("Sorted Segments:", result[0])
        self.assertIn("Sorted Words:", result[0])

    def test_file_count_in_directory(self):
        file_count = FileCountInDirectory()
        with unittest.mock.patch('os.listdir') as mock_listdir:
            mock_listdir.return_value = ['file1.txt', 'file2.jpg', 'file3.png']
            result = file_count.count_files_in_directory("/fake/path", "*.txt,*.jpg")
            self.assertEqual(result, (2,))

if __name__ == '__main__':
    unittest.main()