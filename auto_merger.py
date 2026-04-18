#!/usr/bin/env python3
"""
Auto Merger for Endfield Card Library
Converts new.json from JavaScript format and merges data into equipments.json and suits.json
Handles errors gracefully with detailed reporting.
"""

import json
import re
import sys
import os
from pathlib import Path
from typing import Dict, Any, Tuple, List
from datetime import datetime

class AutoMerger:
    def __init__(self, base_dir: str = "."):
        self.base_dir = Path(base_dir)
        self.new_file = self.base_dir / "new.json"
        self.new_wep_file = self.base_dir / "new_wep.json"
        self.equipments_file = self.base_dir / "endfield" / "assets" / "equipments.json"
        self.suits_file = self.base_dir / "endfield" / "assets" / "suits.json"
        self.weapons_file = self.base_dir / "endfield" / "assets" / "weapons.json"
        
        self.stats = {
            'items_added': 0,
            'items_updated': 0,
            'items_skipped': 0,
            'items_errors': 0,
            'suits_added': 0,
            'suits_updated': 0,
            'suits_skipped': 0,
            'suits_errors': 0,
            'weapons_added': 0,
            'weapons_updated': 0,
            'weapons_skipped': 0,
            'weapons_errors': 0,
        }
        self.errors = []
        self.warnings = []
        
    def log_error(self, msg: str):
        """Log an error message"""
        self.errors.append(msg)
        print(f"❌ ERROR: {msg}")
    
    def log_warning(self, msg: str):
        """Log a warning message"""
        self.warnings.append(msg)
        print(f"⚠️  WARNING: {msg}")
    
    def log_info(self, msg: str):
        """Log an info message"""
        print(f"ℹ️  {msg}")
    
    def log_success(self, msg: str):
        """Log a success message"""
        print(f"✓ {msg}")
    
    def parse_javascript(self, js_content: str) -> Dict[str, Any]:
        """
        Convert JavaScript object notation to valid JSON
        Handles:
        - Unquoted keys (alphanumeric and numeric)
        - Scientific notation (3e3)
        - Decimal numbers starting with dot (.23)
        - Trailing commas
        """
        try:
            json_str = js_content
            
            # 1. Replace alphanumeric keys with quoted keys
            json_str = re.sub(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\s*:', r'"\1":', json_str)
            
            # 2. Replace numeric keys including scientific notation (after object delimiters)
            json_str = re.sub(r'(\{|,)\s*(\d+(?:[eE][+-]?\d+)?)\s*:', r'\1 "\2":', json_str)
            
            # 3. Fix decimal numbers starting with dot
            json_str = re.sub(r'([\[\:,\s])\.(\d)', r'\g<1>0.\2', json_str)
            
            # 4. Remove trailing commas before closing braces/brackets
            json_str = re.sub(r',(\s*[}\]])', r'\1', json_str)
            
            # 5. Parse the JSON
            data = json.loads(json_str)
            self.log_success(f"Parsed new.json successfully")
            return data
            
        except json.JSONDecodeError as e:
            self.log_error(f"Failed to parse new.json: {e}")
            raise
        except Exception as e:
            self.log_error(f"Unexpected error parsing new.json: {e}")
            raise
    
    def load_file(self, filepath: Path) -> Dict[str, Any]:
        """Load a JSON file with error handling"""
        try:
            if not filepath.exists():
                self.log_warning(f"File not found: {filepath}, creating empty dict")
                return {}
            
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.log_success(f"Loaded {filepath.name} ({len(data)} items)")
            return data
            
        except json.JSONDecodeError as e:
            self.log_error(f"Invalid JSON in {filepath}: {e}")
            raise
        except Exception as e:
            self.log_error(f"Failed to load {filepath}: {e}")
            raise
    
    def save_file(self, filepath: Path, data: Dict[str, Any], backup: bool = True) -> bool:
        """Save a JSON file with backup"""
        try:
            # Create backup
            if backup and filepath.exists():
                backup_path = filepath.with_suffix('.json.backup')
                with open(filepath, 'r', encoding='utf-8') as f:
                    backup_content = f.read()
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(backup_content)
                self.log_info(f"Created backup: {backup_path.name}")
            
            # Save file
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            self.log_success(f"Saved {filepath.name} ({len(data)} items)")
            return True
            
        except Exception as e:
            self.log_error(f"Failed to save {filepath}: {e}")
            return False
    
    def process_equipment_item(self, item_id: str, item_data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert equipment item from JS format to JSON format"""
        try:
            json_item = {
                'rarity': item_data.get('Rarity'),
                'icon': item_data.get('Icon'),
                'suit_id': item_data.get('SuitId', ''),
            }
            
            # Convert AttrModifiers to attr_modifiers
            if 'AttrModifiers' in item_data:
                attr_mods = []
                for mod in item_data['AttrModifiers']:
                    attr_mod = {
                        'attr_type': mod.get('AttrType'),
                        'formula': mod.get('Formula'),
                        'values': mod.get('Values', [])
                    }
                    attr_mods.append(attr_mod)
                json_item['attr_modifiers'] = attr_mods
            
            # Add slug if available
            if 'slug' not in json_item and item_data.get('Icon'):
                icon_parts = item_data['Icon'].split('/')
                if icon_parts:
                    json_item['slug'] = icon_parts[-1].replace('.png', '')
            
            return json_item
            
        except Exception as e:
            self.log_error(f"Failed to process equipment item {item_id}: {e}")
            self.stats['items_errors'] += 1
            return None
    
    def merge_equipment(self, new_items: Dict[str, Any], existing_equipments: Dict[str, Any]) -> Dict[str, Any]:
        """Merge new equipment items into existing equipment data"""
        self.log_info("Starting equipment merge...")
        
        for item_id, item_data in new_items.items():
            try:
                # Skip if data is incomplete
                if not isinstance(item_data, dict):
                    self.log_warning(f"Skipping item {item_id}: invalid data type")
                    self.stats['items_skipped'] += 1
                    continue
                
                # Process the item
                processed_item = self.process_equipment_item(item_id, item_data)
                
                if processed_item is None:
                    self.stats['items_skipped'] += 1
                    continue
                
                # Check if item exists
                if item_id in existing_equipments:
                    if existing_equipments[item_id] != processed_item:
                        existing_equipments[item_id] = processed_item
                        self.stats['items_updated'] += 1
                    else:
                        self.stats['items_skipped'] += 1
                else:
                    existing_equipments[item_id] = processed_item
                    self.stats['items_added'] += 1
            
            except Exception as e:
                self.log_error(f"Error processing item {item_id}: {e}")
                self.stats['items_errors'] += 1
        
        return existing_equipments
    
    def merge_suits(self, new_suits: Dict[str, Any], existing_suits: Dict[str, Any]) -> Dict[str, Any]:
        """Merge new suits into existing suit data"""
        self.log_info("Starting suits merge...")
        
        for suit_id, suit_data in new_suits.items():
            try:
                # Skip if data is incomplete
                if not isinstance(suit_data, dict):
                    self.log_warning(f"Skipping suit {suit_id}: invalid data type")
                    self.stats['suits_skipped'] += 1
                    continue
                
                if suit_id in existing_suits:
                    # Update skill_id if available and different
                    if 'SkillId' in suit_data:
                        skill_id = suit_data['SkillId']
                        if existing_suits[suit_id].get('skill_id') != skill_id:
                            existing_suits[suit_id]['skill_id'] = skill_id
                            self.stats['suits_updated'] += 1
                        else:
                            self.stats['suits_skipped'] += 1
                    else:
                        self.stats['suits_skipped'] += 1
                else:
                    # Add new suit with available data
                    new_suit = {
                        'skill_id': suit_data.get('SkillId'),
                        'icon': suit_data.get('Icon'),
                        'name_hash': suit_data.get('NameHash', '')
                    }
                    existing_suits[suit_id] = new_suit
                    self.stats['suits_added'] += 1
            
            except Exception as e:
                self.log_error(f"Error processing suit {suit_id}: {e}")
                self.stats['suits_errors'] += 1
        
        return existing_suits
    
    def process_weapon(self, weapon_id: str, weapon_data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert weapon from JS format to JSON format"""
        try:
            json_weapon = {
                'rarity': weapon_data.get('Rarity'),
                'weapon_type': weapon_data.get('WeaponType'),
                'icon': weapon_data.get('Icon'),
                'name_hash': weapon_data.get('NameHash'),
            }
            
            # Add optional fields if present
            if 'LevelTemplateId' in weapon_data:
                json_weapon['level_template_id'] = weapon_data['LevelTemplateId']
            
            if 'BreakthroughTemplateId' in weapon_data:
                json_weapon['breakthrough_template_id'] = weapon_data['BreakthroughTemplateId']
            
            if 'TalentTemplateId' in weapon_data:
                json_weapon['talent_template_id'] = weapon_data['TalentTemplateId']
            
            if 'SkillList' in weapon_data:
                json_weapon['skill_list'] = weapon_data['SkillList']
            
            # Add slug if available from icon
            if 'slug' not in json_weapon and weapon_data.get('Icon'):
                icon_parts = weapon_data['Icon'].split('/')
                if icon_parts:
                    json_weapon['slug'] = icon_parts[-1].replace('.png', '')
            
            return json_weapon
            
        except Exception as e:
            self.log_error(f"Failed to process weapon {weapon_id}: {e}")
            self.stats['weapons_errors'] += 1
            return None
    
    def merge_weapons(self, new_weapons: Dict[str, Any], existing_weapons: Dict[str, Any]) -> Dict[str, Any]:
        """Merge new weapons into existing weapon data"""
        self.log_info("Starting weapons merge...")
        
        for weapon_id, weapon_data in new_weapons.items():
            try:
                # Skip if data is incomplete
                if not isinstance(weapon_data, dict):
                    self.log_warning(f"Skipping weapon {weapon_id}: invalid data type")
                    self.stats['weapons_skipped'] += 1
                    continue
                
                # Process the weapon
                processed_weapon = self.process_weapon(weapon_id, weapon_data)
                
                if processed_weapon is None:
                    self.stats['weapons_skipped'] += 1
                    continue
                
                # Check if weapon exists
                if weapon_id in existing_weapons:
                    if existing_weapons[weapon_id] != processed_weapon:
                        existing_weapons[weapon_id] = processed_weapon
                        self.stats['weapons_updated'] += 1
                    else:
                        self.stats['weapons_skipped'] += 1
                else:
                    existing_weapons[weapon_id] = processed_weapon
                    self.stats['weapons_added'] += 1
            
            except Exception as e:
                self.log_error(f"Error processing weapon {weapon_id}: {e}")
                self.stats['weapons_errors'] += 1
        
        return existing_weapons
    
    def run(self) -> bool:
        """Execute the merge process"""
        print("\n" + "="*60)
        print("🔄 ENDFIELD AUTO MERGER")
        print("="*60 + "\n")
        
        try:
            # Step 1: Load and process new.json for equipment/suits
            print("Step 1: Loading new.json...")
            with open(self.new_file, 'r', encoding='utf-8', errors='ignore') as f:
                js_content = f.read()
            
            if not js_content.strip():
                self.log_error("new.json is empty")
                return False
            
            # Step 2: Parse JavaScript to JSON
            print("\nStep 2: Converting new.json JavaScript format to JSON...")
            new_data = self.parse_javascript(js_content)
            
            if 'Items' not in new_data or 'Suits' not in new_data:
                self.log_warning("new.json missing 'Items' or 'Suits' key, using available data")
                if 'Items' not in new_data:
                    new_data['Items'] = {}
                if 'Suits' not in new_data:
                    new_data['Suits'] = {}
            
            # Step 3: Load and process new_wep.json for weapons
            new_wep_data = {}
            if self.new_wep_file.exists():
                print("\nStep 3a: Loading new_wep.json...")
                with open(self.new_wep_file, 'r', encoding='utf-8', errors='ignore') as f:
                    wep_js_content = f.read()
                
                if wep_js_content.strip():
                    print("Step 3b: Converting new_wep.json JavaScript format to JSON...")
                    new_wep_data = self.parse_javascript(wep_js_content)
                    self.log_success(f"Loaded new_wep.json ({len(new_wep_data)} weapons)")
                else:
                    self.log_warning("new_wep.json is empty, skipping weapons merge")
            else:
                self.log_warning(f"new_wep.json not found at {self.new_wep_file}, skipping weapons merge")
            
            # Step 4: Load existing files
            print("\nStep 4: Loading existing data files...")
            existing_equipments = self.load_file(self.equipments_file)
            existing_suits = self.load_file(self.suits_file)
            existing_weapons = self.load_file(self.weapons_file)
            
            # Step 5: Merge equipment
            print("\nStep 5: Merging equipment items...")
            existing_equipments = self.merge_equipment(new_data['Items'], existing_equipments)
            
            # Step 6: Merge suits
            print("\nStep 6: Merging suits...")
            existing_suits = self.merge_suits(new_data['Suits'], existing_suits)
            
            # Step 7: Merge weapons (if new_wep_data is available)
            if new_wep_data:
                print("\nStep 7: Merging weapons...")
                existing_weapons = self.merge_weapons(new_wep_data, existing_weapons)
            else:
                print("\nStep 7: Skipping weapons merge (no data)")
            
            # Step 8: Save updated files
            print("\nStep 8: Saving updated files...")
            success = True
            success &= self.save_file(self.equipments_file, existing_equipments)
            success &= self.save_file(self.suits_file, existing_suits)
            if new_wep_data:
                success &= self.save_file(self.weapons_file, existing_weapons)
            
            if not success:
                return False
            
            # Step 9: Print summary
            self._print_summary()
            return True
        
        except Exception as e:
            self.log_error(f"Fatal error: {e}")
            self._print_summary()
            return False
    
    def _print_summary(self):
        """Print merge summary"""
        print("\n" + "="*60)
        print("📊 MERGE SUMMARY")
        print("="*60)
        
        print(f"\n📦 Equipment Items:")
        print(f"   Added:   {self.stats['items_added']}")
        print(f"   Updated: {self.stats['items_updated']}")
        print(f"   Skipped: {self.stats['items_skipped']}")
        if self.stats['items_errors'] > 0:
            print(f"   Errors:  {self.stats['items_errors']}")
        
        print(f"\n🎯 Suits:")
        print(f"   Added:   {self.stats['suits_added']}")
        print(f"   Updated: {self.stats['suits_updated']}")
        print(f"   Skipped: {self.stats['suits_skipped']}")
        if self.stats['suits_errors'] > 0:
            print(f"   Errors:  {self.stats['suits_errors']}")
        
        print(f"\n⚔️  Weapons:")
        print(f"   Added:   {self.stats['weapons_added']}")
        print(f"   Updated: {self.stats['weapons_updated']}")
        print(f"   Skipped: {self.stats['weapons_skipped']}")
        if self.stats['weapons_errors'] > 0:
            print(f"   Errors:  {self.stats['weapons_errors']}")
        
        if self.warnings:
            print(f"\n⚠️  Warnings ({len(self.warnings)}):")
            for warning in self.warnings[:5]:
                print(f"   - {warning}")
            if len(self.warnings) > 5:
                print(f"   ... and {len(self.warnings) - 5} more")
        
        if self.errors:
            print(f"\n❌ Errors ({len(self.errors)}):")
            for error in self.errors[:5]:
                print(f"   - {error}")
            if len(self.errors) > 5:
                print(f"   ... and {len(self.errors) - 5} more")
        
        total_items = self.stats['items_added'] + self.stats['items_updated'] + self.stats['items_skipped'] + self.stats['items_errors']
        total_suits = self.stats['suits_added'] + self.stats['suits_updated'] + self.stats['suits_skipped'] + self.stats['suits_errors']
        total_weapons = self.stats['weapons_added'] + self.stats['weapons_updated'] + self.stats['weapons_skipped'] + self.stats['weapons_errors']
        
        print(f"\n📈 Total Processing:")
        print(f"   Items:   {total_items} items processed")
        print(f"   Suits:   {total_suits} suits processed")
        print(f"   Weapons: {total_weapons} weapons processed")
        
        success = (self.stats['items_errors'] == 0 and self.stats['suits_errors'] == 0 and self.stats['weapons_errors'] == 0)
        status = "✓ SUCCESS" if success else "❌ COMPLETED WITH ERRORS"
        print(f"\n{status}")
        print("="*60 + "\n")
        
        return success


def main():
    """Main entry point"""
    try:
        merger = AutoMerger()
        
        # Validate files exist
        if not merger.new_file.exists():
            print(f"❌ ERROR: new.json not found at {merger.new_file}")
            return 1
        
        # Run merger
        success = merger.run()
        
        return 0 if success else 1
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Merger interrupted by user")
        return 130
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
