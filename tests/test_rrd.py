from collectd_rest import rrd
from django.test import TestCase

class RRDTest(TestCase):
	def test_split1(self):
		ret = rrd.split("abc")
		self.assertListEqual([b'abc',], ret)
	def test_split2(self):
		ret = rrd.split("do\"not\"separate")
		self.assertListEqual([b'donotseparate',], ret)
	def test_split3(self):
		ret = rrd.split("do'not'separate")
		self.assertListEqual([b'donotseparate',], ret)
	def test_split4(self):
		ret = rrd.split("\"\"")
		self.assertListEqual([b'',], ret)
	def test_split5(self):
		ret = rrd.split("\"a b c\"")
		self.assertListEqual([b'a b c',], ret)
	def test_split6(self):
		ret = rrd.split("\"a \\\" c\"")
		self.assertListEqual([b"a \" c",], ret)
	def test_split7(self):
		ret = rrd.split("\"a \\\\ c\"")
		self.assertListEqual([b"a \\ c",], ret)
	def test_split8(self):
		# The escape characters retain its special meaning only when
		# followed by the quote in use, or the escape character itself.
		# Otherwise the escape character will be considered a normal
		# character.
		ret = rrd.split("\"a \\b c\"")
		self.assertListEqual([b"a \\b c",], ret)
		ret = rrd.split("'a \\\" c'")
		self.assertListEqual([b'a \\\" c'], ret)
		ret = rrd.split("'a \\\' c'")
		self.assertListEqual([b'a \' c'], ret)
	def test_split9(self):
		ret = rrd.split("\\b")
		self.assertListEqual([b'b'], ret)
	def test_split10(self):
		ret = rrd.split("a b c")
		self.assertListEqual([b'a', b'b', b'c'], ret)
	def test_split11(self):
		ret = rrd.split("\"a 'b' c\"")
		self.assertListEqual([b'a \'b\' c'], ret)
	def test_split12(self):
		ret = rrd.split("'a \"b\" c'")
		self.assertListEqual([b'a "b" c'], ret)
