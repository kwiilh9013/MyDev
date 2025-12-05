# -*- encoding: utf-8 -*-
import re

class TypingHandler(object):
	def __init__(self, text):
		result = self._SplitGroup(text)
		self._current = ''
		self._splited = []
		self._index = -1
		self._length = 0
		if result and len(result) > 0:
			for item in result:
				temp = self._SplitSingleWord(item[1])
				self._splited.append({
					'code': item[0],
					'chars': temp,
				})
				self._length += len(temp)
				if item[0] == '§z':
					self._length += 1
		else:
			temp = self._SplitSingleWord(text)
			self._splited.append({
				'code': '',
				'chars': temp,
			})
			self._length += len(temp)
		self.Reset()

	@property
	def Index(self):
		return self._index

	@property
	def Current(self):
		return self._current

	@property
	def Length(self):
		return self._length

	def Reset(self):
		self._index = -1
		self._current = ''

	def Next(self):
		ret = None
		index = self._index + 1
		if index < self._length:
			cur = 0
			for item in self._splited:
				code = item['code']
				length = len(item['chars'])
				temp = cur + length
				if code == '§z':
					temp += 1
				if index < temp:
					_index = index - cur
					if 0 <= _index < length:
						ret = code + item['chars'][_index]
					else:
						ret = ''
					break
				cur = temp
		if ret is not None:
			self._index = index
			self._current += ret
		return ret

	def _SplitGroup(self, text):
		ret = []
		i = 0
		unicode_text = text.decode('utf-8')
		code = ''
		text = ''
		while i < len(unicode_text):
			char = unicode_text[i].encode('utf-8')
			if char == '§':
				ret.append((code, text))
				code = char
				text = ''
			elif code == '§':
				code += char
			else:
				text += char
			i += 1
		if len(text) > 0:
			ret.append((code, text))
		return ret


	def _SplitSingleWord(self, text):
		ret = []
		i = 0
		unicode_text = text.decode('utf-8')
		while i < len(unicode_text):
			ret.append(unicode_text[i].encode('utf-8'))
			i += 1
		return ret

