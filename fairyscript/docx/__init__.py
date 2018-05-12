# encoding: utf-8

from .api import Document  # noqa

__version__ = '0.8.5'


# register custom Part classes with opc package reader

from .opc.constants import CONTENT_TYPE as CT, RELATIONSHIP_TYPE as RT
from .opc.part import PartFactory
from .opc.parts.coreprops import CorePropertiesPart

from .parts.document import DocumentPart
from .parts.image import ImagePart
from .parts.numbering import NumberingPart
from .parts.styles import StylesPart


def part_class_selector(content_type, reltype):
    if reltype == RT.IMAGE:
        return ImagePart
    return None


PartFactory.part_class_selector = part_class_selector
PartFactory.part_type_for[CT.OPC_CORE_PROPERTIES] = CorePropertiesPart
PartFactory.part_type_for[CT.WML_DOCUMENT_MAIN] = DocumentPart
PartFactory.part_type_for[CT.WML_NUMBERING] = NumberingPart
PartFactory.part_type_for[CT.WML_STYLES] = StylesPart

del (
    CT, CorePropertiesPart, DocumentPart, NumberingPart, PartFactory,
    StylesPart, part_class_selector
)
