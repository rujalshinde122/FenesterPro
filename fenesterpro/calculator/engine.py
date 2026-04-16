"""Window Calculator Engine."""
import logging
from typing import Dict, Any, Tuple
from projects.models import WindowEntry, ComputedCutPiece
from catalog.models import CuttingRule, HardwareRule

logger = logging.getLogger(__name__)

class WindowCalculator:
    """
    Computes cut lists and hardware requirements for a given WindowEntry.
    """
    
    def calculate(self, window_entry: WindowEntry) -> Tuple[bool, str]:
        """
        Runs calculation for a single window entry.
        
        Args:
            window_entry: The WindowEntry instance to calculate.
            
        Returns:
            Tuple of (Success: bool, Message: str).
        """
        try:
            # 1. Prepare evaluation context
            # We add basic math or leave it strict to the list. I'll use strict arithmetic.
            context = {
                'width': window_entry.width,
                'height': window_entry.height,
                'num_panels': 2, # Default for sliding, we can expand later
                'num_tracks': 2, # Default for sliding
            }
            
            # Additional attributes based on typology (if we extend the model later)
            if 'sliding' in window_entry.typology.category:
                if '3' in window_entry.typology.code:
                    context['num_panels'] = 3
                    context['num_tracks'] = 3
            
            # Fetch rules
            rules = window_entry.typology.cutting_rules.select_related('profile').prefetch_related('deductions').all()
            
            if not rules.exists():
                return False, f"No cutting rules found for typology: {window_entry.typology.code}"
                
            # Keep track of computed pieces to insert in bulk or one by one
            pieces_to_create = []
            
            # Delete old computed pieces for this window if any exist (re-calculation)
            window_entry.cut_pieces.all().delete()
            
            # 2. Evaluate Cutting Rules
            for rule in rules:
                rule_context = context.copy()
                # Load deductions
                for deduction in rule.deductions.all():
                    rule_context[deduction.variable_name] = deduction.value
                
                try:
                    # Evaluate length
                    length_val = eval(rule.length_formula, {"__builtins__": None}, rule_context)
                    # Evaluate quantity
                    qty_val = eval(rule.quantity_formula, {"__builtins__": None}, rule_context)
                    
                    if qty_val > 0 and length_val > 0:
                        pieces_to_create.append(ComputedCutPiece(
                            window=window_entry,
                            profile=rule.profile,
                            piece_name=rule.piece_name,
                            length=float(length_val),
                            quantity=int(qty_val),
                            total_length=float(length_val) * int(qty_val) * window_entry.quantity
                        ))
                except Exception as e:
                    logger.error(f"Error evaluating rule {rule.id} for window {window_entry.id}: {str(e)}")
                    return False, f"Formula error in rule '{rule.piece_name}': {str(e)}"
            
            # 3. Bulk Create Pieces
            if pieces_to_create:
                ComputedCutPiece.objects.bulk_create(pieces_to_create)
                
            # 4. Mark as computed
            window_entry.computed = True
            window_entry.save(update_fields=['computed'])
            
            return True, "Calculation successful"
            
        except Exception as e:
            logger.exception(f"Unexpected error calculating window {window_entry.id}: {str(e)}")
            return False, f"Calculation failed: {str(e)}"
