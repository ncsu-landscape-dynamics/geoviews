import param
from holoviews.core import CompositeOverlay, Element


def _get_projection(el):
    """
    Get coordinate reference system from non-auxiliary elements.
    Return value is a tuple of a precedence integer and the projection,
    to allow non-auxiliary components to take precedence.
    """
    result = None
    if hasattr(el, 'crs'):
        result = (int(el._auxiliary_component), el.crs)
    return result


class ProjectionPlot(param.Parameterized):
    """
    Implements custom _get_projection method to make the coordinate
    reference system available to HoloViews plots as a projection.
    """

    infer_projection = param.Boolean(default=True, doc="""
        Whether the projection should be inferred from the element crs.""")

    def _get_projection(self, obj):
        # Look up custom projection in options
        isoverlay = lambda x: isinstance(x, CompositeOverlay)
        opts = self._traverse_options(obj, 'plot', ['projection', 'infer_projection'],
                                      [CompositeOverlay, Element],
                                      keyfn=isoverlay, defaults=False)
        from_overlay = not all(p is None for p in opts[True]['projection'])
        projections = opts[from_overlay]['projection']
        infer = any(opts[from_overlay]['infer_projection']) or self.infer_projection
        custom_projs = [p for p in projections if p is not None]

        if len(set([type(p) for p in custom_projs])) > 1:
            raise Exception("An axis may only be assigned one projection type")
        elif custom_projs:
            return custom_projs[0]
        if not infer:
            return self.projection

        # If no custom projection is supplied traverse object to get
        # the custom projections and sort by precedence
        projections = sorted([p for p in obj.traverse(_get_projection, [Element])
                              if p is not None and p[1] is not None])
        if projections:
            return projections[0][1]
        else:
            return None
