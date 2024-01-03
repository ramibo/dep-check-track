print("This will be the converter for the BOM from json to cyclonedx json")

# This file is part of CycloneDX Python Lib
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) OWASP Foundation. All Rights Reserved.

import sys

from packageurl import PackageURL

from cyclonedx.exception import MissingOptionalDependencyException
from cyclonedx.factory.license import LicenseFactory
from cyclonedx.model import OrganizationalEntity, XsUri
from cyclonedx.model.bom import Bom
from cyclonedx.model.component import Component, ComponentType, HashType,HashAlgorithm
from cyclonedx.output import make_outputter
from cyclonedx.output.json import JsonV1Dot5
from cyclonedx.schema import SchemaVersion, OutputFormat
from cyclonedx.validation.json import JsonStrictValidator
from cyclonedx.validation import make_schemabased_validator

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cyclonedx.output.json import Json as JsonOutputter
    from cyclonedx.output.xml import Xml as XmlOutputter
    from cyclonedx.validation.xml import XmlValidator


lc_factory = LicenseFactory()

# region build the BOM
# '/tmp/jenkins/home/workspace/test/target/dependency-check-report.json'
json_file_path = sys.argv[1]
json_file= json_file_path

import json
with open(json_file, 'r') as f:
    data = json.load(f)

bom = Bom()
bom.metadata.component = root_component = Component(
    name=data['projectInfo']['artifactID'],
    type=ComponentType.APPLICATION,
    licenses=[lc_factory.make_from_string('MIT')],
    bom_ref=data['projectInfo']['artifactID'],
)
for dependency in data['dependencies']:
    if 'packages' in dependency:
        if 'pkg:maven' in dependency['packages'][0]['id']:
            maven_string = dependency['packages'][0]['id']

            # Split the string based on '/'
            split_parts = maven_string.split('/')

            package_type=split_parts[0].split(':')[1]

            # Extract the relevant information
            group_id = split_parts[1]
            artifact_id_version = split_parts[2]

            # Further split artifact_id_version based on '@'
            artifact_id, version = artifact_id_version.split('@')

            # Extract the license
            try:
                license=dependency['license']
            except:
                license='NA'

            component = Component(
                type=ComponentType.LIBRARY,
                name=dependency['fileName'],
                version=version,
                licenses=[lc_factory.make_from_string(license)],
                # bom_ref=dependency['filePath'], #Todo check why itwon't work
                purl=PackageURL(name=artifact_id, type=package_type, namespace=group_id, version=version),
                hashes=[HashType(alg=HashAlgorithm.SHA_1, content=dependency.get('sha1')),
                        HashType(alg=HashAlgorithm.SHA_256, content=dependency.get('sha256')),
                        HashType(alg=HashAlgorithm.MD5, content=dependency.get('md5'))],
            )

            bom.components.add(component)
            bom.register_dependency(root_component, [component])



# region JSON
"""demo with explicit instructions for SchemaVersion, outputter and validator"""

my_json_outputter: 'JsonOutputter' = JsonV1Dot5(bom)
serialized_json = my_json_outputter.output_as_string(indent=2)
print(serialized_json)
my_json_validator = JsonStrictValidator(SchemaVersion.V1_5)
try:
    validation_errors = my_json_validator.validate_str(serialized_json)
    if validation_errors:
        print('JSON invalid', 'ValidationError:', repr(validation_errors), sep='\n', file=sys.stderr)
        sys.exit(2)
    print('JSON valid')
    with open('bom-test.json', 'w') as f:
        f.write(serialized_json)
except MissingOptionalDependencyException as error:
    print('JSON-validation was skipped due to', error)

print('', '=' * 30, '', sep='\n')