from nodes.fw_nodes import CountTokens, FileCountInDirectory,TokenCountRanker,TrimToTokens

NODE_CLASS_MAPPINGS = {
    "Count Tokens (FW)": CountTokens,
    "Trim To Tokens (FW)": TrimToTokens,
    "Token Count Ranker(FW)": TokenCountRanker,
    "Count Files in Directory (FW)": FileCountInDirectory

}
