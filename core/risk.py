import config

def calculate_tp_sl(side, entry_price):
    if side == 'LONG':
        tp = entry_price * (1 + config.TP_PERCENT)
        sl = entry_price * (1 - config.SL_PERCENT)
    else: # SHORT
        tp = entry_price * (1 - config.TP_PERCENT)
        sl = entry_price * (1 + config.SL_PERCENT)
    return round(tp, 2), round(sl, 2)