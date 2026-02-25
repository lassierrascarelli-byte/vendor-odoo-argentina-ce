from lxml import etree


def _get_response_info(xml_response):
    """
    Parse XML response and return a callable similar to previous SimpleXMLElement usage:
        xml("TagName") -> first text content for that tag (namespace-agnostic)
    """
    if isinstance(xml_response, bytes):
        data = xml_response
    else:
        data = (xml_response or "").encode("utf-8", errors="ignore")

    parser = etree.XMLParser(recover=True, huge_tree=True)
    root = etree.fromstring(data, parser=parser)

    def get(tag_name: str):
        # Namespace-agnostic search by local-name()
        res = root.xpath(f"//*[local-name()='{tag_name}']/text()")
        return res[0] if res else None

    return get


def get_invoice_number_from_response(xml_response, afip_ws="wsfe"):
    if not xml_response:
        return False
    try:
        xml = _get_response_info(xml_response)
        value = xml("CbteDesde")
        return int(value) if value else False
    except Exception:
        return False


def check_invoice_number(account_move):
    pass
