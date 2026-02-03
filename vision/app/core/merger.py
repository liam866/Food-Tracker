import logging
import re
from typing import List, Optional
from app.core.layout import ItemData
from app.schemas import MenuItem

logger = logging.getLogger(__name__)

class Merger:
    def merge(self, items: List[ItemData]) -> List[MenuItem]:
        """
        Merges OCR items into structured MenuItems.
        Sorts by Y coordinate and groups based on heuristics.
        """
        logger.info(f"Merging {len(items)} items...")
        
        # 1. Sort items by Y (top to bottom)
        # Assuming bbox is [x1, y1, x2, y2]
        sorted_items = sorted(items, key=lambda item: item.bbox[1])
        
        menu_items: List[MenuItem] = []
        current_section = "General"
        last_menu_item: Optional[MenuItem] = None
        
        # Regex for price (standalone)
        price_pattern = re.compile(r'^\$?\d+(\.\d{2})?$')
        
        for item in sorted_items:
            text = item.text.strip() if item.text else ""
            if not text:
                continue
                
            # Check for embedded price at the end (e.g., "Burger 22")
            embedded_price_match = re.search(r'\s+(\$?\d+(\.\d{2})?)$', text)
            if embedded_price_match:
                price_str = embedded_price_match.group(1)
                name_text = text[:embedded_price_match.start()].strip()
                
                # Create item immediately
                new_item = MenuItem(section=current_section, name=name_text)
                try:
                    new_item.price = float(re.sub(r'[^\d.]', '', price_str))
                except Exception:
                    pass
                
                menu_items.append(new_item)
                last_menu_item = new_item
                logger.debug(f"Created Item (Embedded Price): {name_text} - {new_item.price}")
                continue

            # Heuristic 1: Is it a standalone price?
            is_price = bool(price_pattern.match(text))
            
            # Heuristic 2: Is it a section header?
            # Simple check: Short, no digits, common section words or looks like header
            is_section = False
            common_sections = ["mains", "starters", "desserts", "drinks", "beverages", "entrees", "sides", "salads", "appetizers"]
            if not is_price and len(text) < 30 and not any(char.isdigit() for char in text):
                if text.lower() in common_sections or (text.isupper() and len(text) > 3):
                    is_section = True
            
            if is_section:
                current_section = text
                last_menu_item = None # Reset context
                logger.debug(f"Found Section: {current_section}")
                continue
                
            if is_price:
                # If we have a pending item, assign price
                if last_menu_item and last_menu_item.price is None:
                    try:
                        price_val = float(re.sub(r'[^\d.]', '', text))
                        last_menu_item.price = price_val
                        logger.debug(f"Assigned Price {price_val} to {last_menu_item.name}")
                    except Exception:
                        pass
                else:
                    logger.debug(f"Orphaned price: {text}")
                continue
            
            # Content (Name or Description)
            # If last_menu_item exists AND has no description AND looks like description
            is_desc = False
            if last_menu_item and not last_menu_item.description:
                # Heuristic: Description is often longer, lower case, or contains ingredients (commas)
                if len(text) > 30 or ',' in text or (any(c.islower() for c in text) and not text.istitle()):
                     is_desc = True
            
            if is_desc:
                last_menu_item.description = text
                logger.debug(f"Assigned Description to {last_menu_item.name}")
            else:
                # New Item Name
                new_item = MenuItem(
                    section=current_section,
                    name=text,
                    description=None,
                    price=None
                )
                menu_items.append(new_item)
                last_menu_item = new_item
                logger.debug(f"Created Item: {text}")
                
        logger.info(f"Merge complete. Produced {len(menu_items)} menu items.")
        return menu_items

merger = Merger()
