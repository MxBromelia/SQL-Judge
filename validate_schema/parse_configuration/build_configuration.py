from dataclasses import dataclass, field
from typing import List, Optional
from collections import namedtuple

@dataclass
class ConfigurationBuilder:
    """Group, Validate and Build the Configurations parameters"""
    adapter_module: Optional[str] = None
    adapter_class: Optional[str] = None
    validations_module: Optional[str] = None
    ignore_tables: List[str] = field(default_factory=list)
    export_format: Optional[str] = None
    export_output: Optional[str] = None

    def merge(self, builder: 'ConfigurationBuilder'):
        """ Combine two builders """
        return ConfigurationBuilder(
            adapter_module=builder.adapter_module or self.adapter_module,
            adapter_class=builder.adapter_class or self.adapter_class,
            validations_module=builder.validations_module or self.validations_module,
            ignore_tables=self.ignore_tables + builder.ignore_tables,
            export_format=builder.export_format or self.export_format
        )

    def is_valid(self):
        """Checks validity of Configuration Builder"""
        if self.adapter_module is None:
            return False
        if self.adapter_class is None:
            return False
        if self.validations_module is None:
            return False
        if self.export_format is None:
            return False
        return True