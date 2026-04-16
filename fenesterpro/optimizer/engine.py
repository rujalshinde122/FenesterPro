"""Bar Optimization Engine."""
from typing import List, Dict, Any

class BarOptimiser:
    """
    Optimizes profile cutting using a First-Fit Decreasing (FFD) algorithm.
    """
    def __init__(self, bar_length: float, saw_kerf: float = 3.0):
        self.bar_length = bar_length  # mm
        self.saw_kerf = saw_kerf      # mm lost per cut

    def optimise(self, cut_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Groups pieces by profile code and applies FFD algorithm.
        
        Args:
            cut_list: [{'profile_code': str, 'profile_name': str, 'length': float, 'qty': int}, ...]
            
        Returns:
            Dictionary with optimization statistics and bar layouts.
        """
        # Group pieces by profile code
        grouped_pieces = {}
        for item in cut_list:
            code = item['profile_code']
            if code not in grouped_pieces:
                grouped_pieces[code] = {
                    'profile_name': item['profile_name'],
                    'pieces': []
                }
            # Expand quantities into individual tracking pieces
            for _ in range(item.get('qty', 1)):
                grouped_pieces[code]['pieces'].append({
                    'piece_name': item.get('piece_name', 'Unnamed'),
                    'length': float(item['length'])
                })

        result = {
            'bars_used': 0,
            'waste_mm': 0.0,
            'waste_percent': 0.0,
            'profiles': {}   # Code -> layout details
        }

        total_bars = 0
        total_waste = 0.0
        total_bar_length_used = 0.0

        for code, data in grouped_pieces.items():
            # 1. Sort pieces descending by length (First-Fit Decreasing)
            pieces = sorted(data['pieces'], key=lambda x: x['length'], reverse=True)
            bars = []

            for piece in pieces:
                piece_length = piece['length']
                placed = False
                
                # 2. Try to fit each piece into an existing bar
                for bar in bars:
                    # Calculate required length if adding this piece (piece + kerf if not first)
                    kerf_needed = self.saw_kerf if len(bar['pieces']) > 0 else 0
                    if bar['used_length'] + kerf_needed + piece_length <= self.bar_length:
                        bar['pieces'].append(piece)
                        bar['used_length'] += kerf_needed + piece_length
                        bar['remaining'] -= (kerf_needed + piece_length)
                        placed = True
                        break
                
                # 3. If it doesn't fit, open a new bar
                if not placed:
                    if piece_length > self.bar_length:
                        # Fallback for oversize piece: cannot fit into standard bar. 
                        # In reality, this requires a special order or custom bar.
                        # For now, put it in its own bar with negative remaining.
                        bars.append({
                            'bar_number': len(bars) + 1,
                            'pieces': [piece],
                            'used_length': piece_length,
                            'remaining': self.bar_length - piece_length
                        })
                    else:
                        bars.append({
                            'bar_number': len(bars) + 1,
                            'pieces': [piece],
                            'used_length': piece_length,
                            'remaining': self.bar_length - piece_length
                        })

            profile_waste = sum(b['remaining'] for b in bars)
            total_bars += len(bars)
            total_waste += profile_waste
            total_bar_length_used += len(bars) * self.bar_length

            result['profiles'][code] = {
                'profile_name': data['profile_name'],
                'bars_used': len(bars),
                'waste_mm': profile_waste,
                'bar_layouts': bars
            }

        result['bars_used'] = total_bars
        result['waste_mm'] = total_waste
        if total_bar_length_used > 0:
            result['waste_percent'] = (total_waste / total_bar_length_used) * 100
        else:
            result['waste_percent'] = 0.0

        return result
