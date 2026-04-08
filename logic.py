from datetime import datetime

class NotesManager:
    def __init__(self):
        # Initialize an empty list to store notes
        self.notes = []

    def add_note(self, title, content, tags_string):
        """Note banata hai aur list mein append karta hai."""
        # String ko list mein convert karna (Python logic)
        tags_list = [tag.strip() for tag in tags_string.split(",") if tag.strip()]
        
        note = {
            "id": len(self.notes) + 1,
            "title": title,
            "content": content,
            "tags": tags_list,
            "date": datetime.now().strftime("%d-%b %H:%M")
        }
        self.notes.append(note)
        return True

    def search_notes(self, query):
        """Loop use kar k matching notes dhundta hai."""
        if not query:
            return self.notes
            
        results = []
        for note in self.notes:
            # Title ya Tags mein search karna
            if (query.lower() in note['title'].lower() or 
                any(query.lower() in t.lower() for t in note['tags'])):
                results.append(note)
        return results

    def delete_note(self, note_id):
        """List comprehension se note delete karna."""
        self.notes = [n for n in self.notes if n['id'] != note_id]