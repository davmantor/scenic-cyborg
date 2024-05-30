cyborg = None
try:
    import cyborg
except ImportError:
    pass
if cyborg:
    from .simulator import cyborg
del cyborg