from typing import List
import re


#递归切片+重叠策略
class DocumentChunker:
    def __init__(
        self,
        chunk_size: int = 500,            #每个切片的目标大小（字符数）
        chunk_overlap: int = 50,         #chunk_overlap: 切片之间的重叠字符数
        separators: List[str] = None      #分隔符列表，按优先级排序
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        # 默认分隔符：优先按段落、句子、换行、空格切割
        self.separators = separators or [
            "\n\n",      # 段落分隔
            "\n",        # 换行
            "。|！|？",  # 中文句号
            "\\. |\\! |\\? ",  # 英文句号
            " ",         # 空格
            ""           # 字符级别
        ]

    def chunk(self, document: str) -> List[str]:
        return self._split_text(document, self.separators)

    #递归切片
    def _split_text(self, text: str, separators: List[str]) -> List[str]:
        final_chunks = []
        separator = separators[-1]

        # 找到合适的分隔符
        for _s in separators:
            if _s == "":
                separator = _s
                break
            if re.search(_s, text):      #分隔符是否在文本中出现
                separator = _s
                break

        # 按分隔符切割
        if separator:
            splits = re.split(separator, text)
        else:
            splits = list(text)

        #为了提高效率，合并小块并处理重叠
        good_splits = []        # 临时存储小块，待合并列表
        for s in splits:
            if len(s) < self.chunk_size:
                good_splits.append(s)
            else:      # 如果是大块
                if good_splits:
                    merged_text = self._merge_splits(good_splits, separator)    #先合并先前的小块
                    final_chunks.extend(merged_text)
                    good_splits = []

                other_info = self._split_text(s, separators[separators.index(separator) + 1:])
                final_chunks.extend(other_info)

        if good_splits:
            merged_text = self._merge_splits(good_splits, separator)
            final_chunks.extend(merged_text)

        return [chunk.strip() for chunk in final_chunks if chunk.strip()]

    #合并小块并添加重叠
    def _merge_splits(self, splits: List[str], separator: str) -> List[str]:
        separator_len = len(separator)
        good_splits = []
        current_chunk = []
        current_length = 0

        for s in splits:
            s_len = len(s)

            if current_length + s_len + separator_len > self.chunk_size:     #加入当前块会>目标块大小
                # 当前块已满，保存并开始新块
                if current_chunk:    #存在内容
                    chunk = separator.join(current_chunk)    #合并当前块
                    current_length = len(chunk)
                    good_splits.append(chunk)            #保存到结果列表

                    # 添加重叠机制避免在关键信息边界处被切断（保留最后的部分内容）
                    # 提取重叠块(移除处理)   满足两个条件之一：1. 当前块长度超过重叠大小 2. 当前块长度超过目标块大小 3. 加入当前块会超过目标块大小
                    while (
                        current_length > self.chunk_overlap
                        or (
                            len(current_chunk) > 1
                            and current_length + s_len + separator_len > self.chunk_size
                        )
                    ):
                        current_length -= len(current_chunk[0]) + separator_len      # 减去第一个碎片的长度
                        current_chunk = current_chunk[1:]                            # 移除第一个碎片

            current_chunk.append(s)
            current_length += s_len + separator_len

        # 处理最后一块
        if current_chunk:
            chunk = separator.join(current_chunk)
            good_splits.append(chunk)

        return good_splits
