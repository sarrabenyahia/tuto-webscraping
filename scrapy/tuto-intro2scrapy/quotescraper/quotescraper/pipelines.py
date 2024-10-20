from itemadapter import ItemAdapter
import json
import scrapy

class CleanDataPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        # Nettoyer le texte de la citation
        text = adapter.get('text')
        if text:
            adapter['text'] = text.strip().replace('“', '').replace('”', '')
        
        # Mettre l'auteur en majuscules
        author = adapter.get('author')
        if author:
            adapter['author'] = author.upper()
        
        # S'assurer que les tags sont uniques et en minuscules
        tags = adapter.get('tags')
        if tags:
            adapter['tags'] = list(set([tag.lower() for tag in tags]))
        
        return item

class JsonWriterPipeline:
    def open_spider(self, spider):
        self.file = open('quotes.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict(), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item
    
    def close_spider(self, spider):
        self.file.close()

