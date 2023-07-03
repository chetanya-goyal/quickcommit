from gdsfactory.cell import cell
from gdsfactory.component import Component
from gdsfactory.components.rectangle import rectangle
from PDK.mappedpdk import MappedPDK
from typing import Optional
from via_gen import via_array


@cell
def mimcap(
    pdk: MappedPDK, size=(5.0, 5.0), route_layer: Optional[str] = "met4"
) -> Component:
    """create a mimcap
    args:
    pdk=pdk to use
    size=tuple(float,float) size of cap
    ****Note: size is the size of the capmet layer
    ports:
    top_met_...all edges, this is the metal over the capmet
    """
    # get cap layers and run error checking
    pdk.has_required_glayers(["capmet", route_layer])
    capmettop = pdk.layer_to_glayer(pdk.get_grule("capmet")["capmettop"])
    capmetbottom = pdk.layer_to_glayer(pdk.get_grule("capmet")["capmetbottom"])
    pdk.activate()
    # create top component
    mim_cap = Component()
    mim_cap << rectangle(size=size, layer=pdk.get_glayer("capmet"), centered=True)
    top_met_ref = mim_cap << via_array(
        pdk, capmetbottom, capmettop, size=size, minus1=True
    )
    # flatten and create ports
    mim_cap.add_ports(top_met_ref.get_ports_list())
    mim_cap = mim_cap.flatten()
    return mim_cap


if __name__ == "__main__":
    from PDK.util.standard_main import pdk

    mycap = mimcap(pdk)
    mycap.show()
    for portname in mycap.ports.keys():
        print(portname)
