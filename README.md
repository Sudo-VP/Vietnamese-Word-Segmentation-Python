# word_segmenter
## Chú ý: 
### Bộ mã này được viết lại từ bộ RDRSegmenter: https://github.com/datquocnguyen/RDRsegmenter bằng Python với mục đích thuận tiện hơn cho việc sử dụng và tùy biến các công cụ NLP tiếng Việt
The implementation of RDRsegmenter, as described in [our paper](http://www.lrec-conf.org/proceedings/lrec2018/summaries/55.html):

	@InProceedings{NguyenNVDJ2018,
	author={Dat Quoc Nguyen and Dai Quoc Nguyen and Thanh Vu and Mark Dras and Mark Johnson},
	title={{A Fast and Accurate Vietnamese Word Segmenter}},
	booktitle={Proceedings of the 11th International Conference on Language Resources and Evaluation (LREC 2018)},
	pages={2582--2587},
	year={2018}
	}

**Please CITE** our paper whenever RDRsegmenter is used to produce published results or incorporated into other software. 

Translator: Vinh Pham

## Hướng dẫn sử dụng
** REQUIRED Python3 **
- python setup.py install
- python -m pip install .

## Ví dụ
```
>>> from vws import RDRSegmenter, Tokenizer
>>> rdrsegment = RDRSegmenter.RDRSegmenter()
>>> tokenizer = Tokenizer.Tokenizer()
>>> output = rdrsegment.segmentRawSentences(tokenizer,"Lượng khách Thái bắt đầu gia tăng từ đầu năm 2005. Bên cạnh đó, kể từ tháng 10-2005 đến nay, từ khi được phép của VN, các đoàn caravan của Thái Lan cũng đã ồ ạt đổ vào VN.")
>>> print(output)
```
Output:
```
>>> Lượng khách Thái bắt_đầu gia_tăng từ đầu năm 2005. Bên cạnh đó, kể từ tháng 10-2005 đến nay, từ khi được phép của VN, các đoàn caravan của Thái_Lan cũng đã ồ_ạt đổ vào VN.
```