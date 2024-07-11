import os 


class CountTokens:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "clip": ("CLIP", {"forceInput": True}),
                "text": ('STRING', {"forceInput": True}),
            }
        }

    RETURN_TYPES = ('INT',)
    FUNCTION = "count_tokens"
    CATEGORY = "Fearnworks/Text/Tokens"

    def count_tokens(self, clip, text):
        print("Counting Tokens for text:", text)
        tokens = clip.tokenize(text)

        # Filter out padding tokens (token value is not 0) in the first list of 'g'
        if 'g' in tokens and len(tokens['g']) > 0:
            real_tokens = [token for token in tokens['g'][0] if token[0] != 0]
            token_count = len(real_tokens)
        else:
            token_count = 0

        print(f"Real token count: {token_count}")
        cond, pooled = clip.encode_from_tokens(tokens, return_pooled=True)
        print("Contioned Shape:", cond)
        print("############################")
        print("Pooled Shape:", pooled)

        return (token_count, )
        
    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")

class TrimToTokens:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "clip": ("CLIP", {"forceInput": True}),
                "text": ('STRING', {"forceInput": True}),
                "max_tokens": ('INT', {"forceInput": True})  # Maximum number of tokens allowed
            }
        }

    RETURN_TYPES = ('STRING',)
    FUNCTION = "trim_to_tokens"
    CATEGORY = "Fearnworks/Text/Tokens"

    def trim_to_tokens(self, clip, text, max_tokens):
        print("Trimming text to fit within a specific number of tokens:", max_tokens)

        # Split the text by commas
        segments = text.split(',')
        trimmed_segments = []

        current_token_count = 0
        for segment in segments:
            tokens = clip.tokenize(segment)
            if 'g' in tokens and len(tokens['g']) > 0:
                real_tokens = [token for token in tokens['g'][0] if token[0] != 0]
                segment_token_count = len(real_tokens)
            else:
                segment_token_count = 0

            if current_token_count + segment_token_count <= max_tokens:
                trimmed_segments.append(segment)
                current_token_count += segment_token_count
            else:
                break  # Stop adding segments once the max token count is reached or exceeded

        # Join the segments to form the trimmed text
        trimmed_text = ','.join(trimmed_segments)

        print(f"Trimmed text: {trimmed_text}")
        return (trimmed_text, )

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")
    
class TokenCountRanker:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "clip": ("CLIP", {"forceInput": True}),
                "text": ('STRING', {"forceInput": True}),
            }
        }

    RETURN_TYPES = ('STRING',)
    FUNCTION = "sort_segments_and_words_by_token_count"
    CATEGORY = "Fearnworks/Text/Tokens"

    def sort_segments_and_words_by_token_count(self, clip, text):
        print("Sorting segments and words by token count for text:", text)

        # Split the text by commas and tokenize each segment
        segments = text.split(',')
        segment_token_info = []
        word_token_info = []

        for segment in segments:
            words = segment.strip().split()
            segment_total_token_count = 0

            for word in words:
                tokens = clip.tokenize(word)
                if 'g' in tokens and len(tokens['g']) > 0:
                    real_tokens = [token for token in tokens['g'][0] if token[0] != 0]
                    word_token_count = len(real_tokens)
                else:
                    word_token_count = 0

                segment_total_token_count += word_token_count
                word_token_info.append((word, word_token_count))

            segment_token_info.append((segment, segment_total_token_count))

        # Sort segments and words by token count in descending order
        sorted_segments = sorted(segment_token_info, key=lambda x: x[1], reverse=True)
        sorted_words = sorted(word_token_info, key=lambda x: x[1], reverse=True)

        # Construct strings with each sorted segment and word and their token counts
        sorted_segments_text = '\n'.join(f"{segment} ({token_count} tokens)" for segment, token_count in sorted_segments)
        sorted_words_text = '\n'.join(f"{word} ({token_count} tokens)" for word, token_count in sorted_words)

        # Combine the two sorted lists into one string
        combined_sorted_text = f"Sorted Segments:\n{sorted_segments_text}\n\nSorted Words:\n{sorted_words_text}"

        print(combined_sorted_text)
        return (combined_sorted_text, )

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")

import fnmatch

class FileCountInDirectory:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "directory_path": ('STRING', {"forceInput": True}),
                "file_types": ('STRING', {"forceInput": True, "default":"*"})
            }
        }

    RETURN_TYPES = ('INT',)
    FUNCTION = "count_files_in_directory"
    CATEGORY = "Fearnworks/File Operations"

    def count_files_in_directory(self, directory_path, file_types):
        print(f"Counting files in directory: {directory_path} with file types: {file_types}")

        file_types_list = file_types.split(',')
        try:
            file_count = sum(
                len(fnmatch.filter(os.listdir(directory_path), pattern.strip()))
                for pattern in file_types_list
            )
        except Exception as e:
            print(f"Error occurred: {e}")
            return (0,)

        print(f"Number of files matching types {file_types}: {file_count}")
        return (file_count,)

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")

# Keep this function for backwards compatibility if needed
def file_count_in_directory(directory_path, file_types):
    count = 0
    for file_type in file_types.split(','):
        count += len(fnmatch.filter(os.listdir(directory_path), file_type.strip()))
    return (count,)