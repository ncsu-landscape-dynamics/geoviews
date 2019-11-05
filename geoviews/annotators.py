import param

import cartopy.crs as ccrs

from holoviews.annotators import (
    Annotator, AnnotationManager, PathAnnotator, PolyAnnotator, PointAnnotator # noqa
)
from holoviews.plotting.links import DataLink, VertexTableLink as hvVertexTableLink
from panel.util import param_name

from .models.custom_tools import CheckpointTool, RestoreTool, ClearTool
from .links import VertexTableLink, PointTableLink
from .operation import project
from .streams import PolyVertexDraw, PolyVertexEdit

Annotator._tools = [CheckpointTool, RestoreTool, ClearTool]
Annotator.table_transforms.append(project.instance(projection=ccrs.PlateCarree()))

def get_point_table_link(self, source, target):
    if hasattr(source, 'crs'):
        return PointTableLink(source, target)
    else:
        return DataLink(source, target)

PointAnnotator._point_table_link = get_point_table_link

def get_vertex_table_link(self, source, target):
    if hasattr(source, 'crs'):
        return VertexTableLink(source, target)
    else:
        return hvVertexTableLink(source, target)

PathAnnotator._vertex_table_link = get_vertex_table_link
PolyAnnotator._vertex_table_link = get_vertex_table_link

def initialize_tools(plot, element):
    """
    Initializes the Checkpoint and Restore tools.
    """
    cds = plot.handles['source']
    checkpoint = plot.state.select(type=CheckpointTool)
    restore = plot.state.select(type=RestoreTool)
    clear = plot.state.select(type=ClearTool)
    if checkpoint:
        checkpoint[0].sources.append(cds)
    if restore:
        restore[0].sources.append(cds)
    if clear:
        clear[0].sources.append(cds)
        
Annotator._extra_opts['hooks'] = [initialize_tools]


class PathBreakingAnnotator(PathAnnotator):

    feature_style = param.Dict(default={'fill_color': 'blue', 'size': 10}, doc="""
         Styling to apply to the feature vertices.""")

    node_style = param.Dict(default={'fill_color': 'indianred', 'size': 6}, doc="""
         Styling to apply to the node vertices.""")

    def _init_table(self):
        name = param_name(self.name)
        style_kwargs = dict(node_style=self.node_style, feature_style=self.feature_style)
        self._stream = PolyVertexDraw(
            source=self.element, data={}, num_objects=self.num_objects,
            show_vertices=self.show_vertices, tooltip='%s Tool' % name,
            **style_kwargs
        )
        if self.edit_vertices:
            self._vertex_stream = PolyVertexEdit(
                source=self.element, tooltip='%s Edit Tool' % name,
                **style_kwargs
            )

        table_data = self._table_data()
        self._table = Table(table_data, list(self.annotations), []).opts(**self.table_opts)
        self._link = DataLink(self.element, self._table)
        self._vertex_table = Table(
            [], self.element.kdims, list(self.vertex_annotations)
        ).opts(**self.table_opts)
        self._vertex_link = VertexTableLink(self.element, self._vertex_table)
        self._tables = [
            ('%s' % name, self._table),
            ('%s Vertices' % name, self._vertex_table)
        ]
