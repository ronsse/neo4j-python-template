from neomodel import StructuredNode, StringProperty, RelationshipTo, ArrayProperty
from models.relationship_models import TimedRel


class Prisma(StructuredNode):
    # Primary
    uid = StringProperty(unique_index=True, required=True)
    # Additional properties
    externalAssetId = StringProperty()
    cloudType = StringProperty()
    createdTs = StringProperty()
    insertTs = StringProperty()
    # Relationships
    server = RelationshipTo("Server", "IS_TRACKED_BY")


class CrowdStrike(StructuredNode):
    # Primary
    device_id = StringProperty(unique_index=True, required=True)
    # Additional properties
    first_seen = StringProperty()
    last_seen = StringProperty()
    # Relationships
    server = RelationshipTo("Server", "IS_TRACKED_BY")


class Cmdb(StructuredNode):
    # Primary
    sys_id = StringProperty(unique_index=True, required=True)
    # Additional properties
    sys_upated_on = StringProperty()
    serial_number = StringProperty()
    qualys_agent_id = StringProperty()
    crowdstrike_agent = StringProperty()
    application_owner = StringProperty()
    # Relationships
    server = RelationshipTo("Server", "IS_TRACKED_BY")


class Qualys(StructuredNode):
    # Primary
    uid = StringProperty(unique_index=True, required=True)
    # Additional properties
    externalAssetId = StringProperty()
    cloudType = StringProperty()
    createdTs = StringProperty()
    insertTs = StringProperty()
    # Relationships
    server = RelationshipTo("Server", "IS_TRACKED_BY")


class Server(StructuredNode):
    # Primary
    hostname = StringProperty(required=True)
    # additional Properties
    name = StringProperty()
    accountGroup = StringProperty()
    assetType = StringProperty()
    accountName = StringProperty()
    resourceType = StringProperty()
    private_ip = StringProperty()
    dns_name = StringProperty()
    # Other properties...

    owner = RelationshipTo("Owner", "IS_OWNED_BY")


class Nic(StructuredNode):
    # Primary
    macAddress = StringProperty(unique_index=True, required=True)
    # Additional properties
    vpcId = StringProperty()
    groups = ArrayProperty(StringProperty())
    status = StringProperty()
    subnetId = StringProperty()
    ownerId = StringProperty()
    privateIpAddress = StringProperty()
    networkInterfaceId = StringProperty()
    privateIpAddresses = ArrayProperty(StringProperty())
    ipv6Addresses = ArrayProperty(StringProperty())
    blockDeviceMappings = ArrayProperty(StringProperty())
    name = StringProperty()
    regionId = StringProperty()
    # relationships
    servers = RelationshipTo("Server", "IS_INSTALLED_ON")


class Owner(StructuredNode):
    # Primary
    name = StringProperty(unique_index=True, required=True)
    # Additional properties
    owner_id = StringProperty()
    team = StringProperty()
    cost_center = StringProperty()
    # Other properties...


class IPAddress(StructuredNode):
    # Primary
    ip_address = StringProperty(unique_index=True, required=True)

    type = StringProperty()
    # types of ip addresses = public, private, gateway,external,local
    # Additional properties
    # Other properties...
    server = RelationshipTo("Server", "IS_USED_BY", model=TimedRel)
