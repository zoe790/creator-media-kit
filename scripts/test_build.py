import json, tempfile, unittest, importlib.util
from pathlib import Path
spec=importlib.util.spec_from_file_location('builder',Path(__file__).with_name('build.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class BuildTests(unittest.TestCase):
 def test_eight_no_photo_and_escaping(self):
  with tempfile.TemporaryDirectory() as td:
   root=Path(td); brief={'profile':{'name':'<script>alert(1)</script>','accounts':[{'platform':'Platform','followers':'12K'}]},'cases':[{'id':'a','kind':'editorial','title':'A&B'}]};src=root/'brief.json';src.write_text(json.dumps(brief));r=m.build(src,root/'out')
   self.assertEqual(len(r['styles']),8)
   for s in r['styles']:
    h=(root/'out'/s['html']).read_text();self.assertNotIn('<script>',h);self.assertNotIn('src=""',h);self.assertIn('no-photo',h);self.assertIn('data-case="a"',h);self.assertIn('A&amp;B',h)
 def test_unassigned_cases_preserved_and_no_fake_brands(self):
  with tempfile.TemporaryDirectory() as td:
   root=Path(td);d={'profile':{'name':'Demo Creator'},'brands':[{'id':'b','name':'NOT_CONFIRMED','confirmed':False}],'cases':[{'id':'a','kind':'editorial'},{'id':'b','kind':'editorial'}],'sections':[{'title':'one','case_ids':['a']}]};src=root/'b.json';src.write_text(json.dumps(d));m.build(src,root/'out','long-table');h=(root/'out/long-table/poster.html').read_text();self.assertIn('data-case="b"',h);self.assertNotIn('NOT_CONFIRMED',h)
 def test_unknown_brand_rejected(self):
  with tempfile.TemporaryDirectory() as td:
   root=Path(td);src=root/'b.json';src.write_text(json.dumps({'profile':{'name':'Demo Creator'},'cases':[{'id':'a','kind':'sponsored','brand_id':'missing'}]}))
   with self.assertRaises(ValueError):m.build(src,root/'out')
 def test_full_preview_and_extra_accounts(self):
  with tempfile.TemporaryDirectory() as td:
   root=Path(td);d={'profile':{'name':'Test Creator','accounts':[{'platform':'Platform'+str(i),'followers':str(i+1)+'K'} for i in range(4)]},'cases':[{'id':str(i),'kind':'editorial'} for i in range(5)]};src=root/'b.json';src.write_text(json.dumps(d));m.build(src,root/'full','navy-creator','full');m.build(src,root/'preview','navy-creator','preview')
   full=(root/'full/navy-creator/poster.html').read_text();preview=(root/'preview/navy-creator/poster.html').read_text();self.assertEqual(full.count('data-case='),5);self.assertEqual(preview.count('data-case='),3);self.assertIn('Platform3 followers',full);self.assertNotIn('unique audience',full)
 def test_compact_brand_default_and_explicit_all(self):
  with tempfile.TemporaryDirectory() as td:
   root=Path(td);d={'profile':{'name':'Test Creator'},'brands':[{'id':str(i),'name':'Brand'+str(i),'confirmed':True} for i in range(9)]};src=root/'b.json';src.write_text(json.dumps(d));r=m.build(src,root/'default','long-table');h=(root/'default/long-table/poster.html').read_text();self.assertEqual(h.count('class="brand-cell"'),6);self.assertIn('Selected brand partners',h);self.assertEqual(r['displayed_brand_count'],6)
   d['settings']={'brand_limit':0};src.write_text(json.dumps(d));r=m.build(src,root/'all','long-table');self.assertEqual(r['displayed_brand_count'],9)
 def test_unknown_content_does_not_imply_brand_relationship(self):
  with tempfile.TemporaryDirectory() as td:
   root=Path(td);src=root/'brief.json';src.write_text(json.dumps({'profile':{'name':'Demo Creator'},'brands':[{'id':'b','name':'UNCONFIRMED_BRAND','confirmed':False}],'cases':[{'id':'a','kind':'unknown','brand_id':'b','title':'Selected post'}]}))
   m.build(src,root/'out','long-table');h=(root/'out/long-table/poster.html').read_text()
   self.assertIn('Content showcase',h);self.assertNotIn('Independent work',h);self.assertNotIn('Brand collaboration',h);self.assertNotIn('UNCONFIRMED_BRAND',h)
 def test_partial_accounts_and_visible_provenance(self):
  with tempfile.TemporaryDirectory() as td:
   root=Path(td);src=root/'brief.json';src.write_text(json.dumps({'profile':{'name':'Demo Creator','accounts':[{'platform':'Hidden Platform'},{'platform':'RedNote','followers':'10K+','as_of':'2026-10-11'}]},'delivery_note':'Public-profile draft <Needs review>'}))
   m.build(src,root/'out','long-table','preview');h=(root/'out/long-table/poster.html').read_text()
   self.assertIn('10K+',h);self.assertNotIn('Hidden Platform followers',h);self.assertIn('2026-10-11',h);self.assertIn('Preview',h);self.assertIn('&lt;Needs review&gt;',h)
if __name__=='__main__':unittest.main()
