import json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class RepositoryTests(unittest.TestCase):
    def test_benefit_ids_unique(self):
        data=json.loads((ROOT/'config/benefits.json').read_text())
        ids=[x['id'] for x in data['benefits']]
        self.assertEqual(len(ids),len(set(ids)))
    def test_official_urls_https(self):
        data=json.loads((ROOT/'config/benefits.json').read_text())
        self.assertTrue(all(x['official_url'].startswith('https://') for x in data['benefits']))
    def test_required_dashboard_files(self):
        for name in ['index.html','style.css','app.js','data/current/benefits.json']:
            self.assertTrue((ROOT/name).exists(),name)
if __name__=='__main__': unittest.main()
