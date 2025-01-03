from __future__ import annotations
from datetime import datetime
import json
from typing import Optional
from pydantic import BaseModel, Field


class InvoiceAddress(BaseModel):
    """
    A class representing an address in an invoice.

    Attributes:
        street: Street address
        city: City, e.g. New York
        state: State, e.g. NY
        postal_code: Postal code, e.g. 10001
        country: Country, e.g. USA
    """

    street: Optional[str] = Field(
        description='Street address, e.g. 123 Main St.'
    )
    city: Optional[str] = Field(
        description='City, e.g. New York'
    )
    state: Optional[str] = Field(
        description='State, e.g. NY'
    )
    postal_code: Optional[str] = Field(
        description='Postal code, e.g. 10001'
    )
    country: Optional[str] = Field(
        description='Country, e.g. USA'
    )

    @staticmethod
    def example():
        """
        Creates an empty example InvoiceAddress object.

        Returns:
            InvoiceAddress: An empty InvoiceAddress object.
        """

        return InvoiceAddress(
            street='',
            city='',
            state='',
            postal_code='',
            country=''
        )

    def to_dict(self):
        """
        Converts the InvoiceAddress object to a dictionary.

        Returns:
            dict: The InvoiceAddress object as a dictionary.
        """

        return {
            'street': self.street,
            'city': self.city,
            'state': self.state,
            'postal_code': self.postal_code,
            'country': self.country
        }


class InvoiceSignature(BaseModel):
    """
    A class representing a signature for an invoice.

    Attributes:
        signatory: Name of the person who signed the invoice.
        is_signed: Indicates if the invoice is signed.
    """

    signatory: Optional[str] = Field(
        description='Name of the person who signed the invoice'
    )
    is_signed: Optional[bool] = Field(
        description='Indicates if the invoice is signed'
    )

    @staticmethod
    def example():
        """
        Creates an empty example InvoiceSignature object.

        Returns:
            InvoiceSignature: An empty InvoiceSignature object
        """

        return InvoiceSignature(
            signatory='',
            is_signed=False
        )

    def to_dict(self):
        """
        Converts the InvoiceSignature object to a dictionary.

        Returns:
            dict: The InvoiceSignature object as a dictionary.
        """

        return {
            'signatory': self.signatory,
            'is_signed': self.is_signed
        }


class InvoiceItem(BaseModel):
    """
    A class representing a line item in an invoice.

    Attributes:
        product_code: Product code, product number, or SKU associated with the line item.
        description: Description of the line item.
        quantity: Quantity of the line item.
        tax: Tax amount applied to the line item.
        tax_rate: Tax rate applied to the line item.
        unit_price: Net or gross price of one unit of the line item.
        total: The total charges associated with the line item.
        reason: Reason for returning the line item.
    """

    product_code: Optional[str] = Field(
        description='Product code, product number, or SKU associated with the line item, e.g. 12345',
    )
    description: Optional[str] = Field(
        description='Description of the line item, e.g. Product A',
    )
    quantity: Optional[int] = Field(
        description='Quantity of the line item',
    )
    tax: Optional[float] = Field(
        description='Tax amount applied to the line item, e.g. 6.00',
    )
    tax_rate: Optional[str] = Field(
        description='Tax rate applied to the line item, e.g. 18%',
    )
    unit_price: Optional[float] = Field(
        description='Net or gross price of one unit of the line item, e.g. 10.00',
    )
    total: Optional[float] = Field(
        description='The total charges associated with the line item, e.g. 100.00',
    )
    reason: Optional[str] = Field(
        description='Reason for returning the line item, e.g. Damaged',
    )

    @staticmethod
    def example():
        """
        Creates an empty example InvoiceItem object.

        Returns:
            InvoiceItem: An empty InvoiceItem object.
        """
        return InvoiceItem(
            product_code='',
            description='',
            quantity=0.0,
            tax=0.0,
            tax_rate='',
            unit_price=0.0,
            total=0.0,
            reason=''
        )

    def to_dict(self):
        """
        Converts the InvoiceItem object to a dictionary.

        Returns:
            dict: The InvoiceItem object as a dictionary.
        """

        return {
            'product_code': self.product_code,
            'description': self.description,
            'quantity': self.quantity,
            'tax': self.tax,
            'tax_rate': self.tax_rate,
            'unit_price': self.unit_price,
            'total': self.total,
            'reason': self.reason
        }


class Invoice(BaseModel):
    """
    A class representing an invoice.

    Attributes:
        customer_name: Name of the customer being invoiced.
        customer_address: Full address of the customer.
        customer_tax_id: Government tax ID of the customer.
        shipping_address: Full address of the shipping location for the customer.
        purchase_order: Purchase order reference number.
        invoice_id: Reference ID for the invoice.
        invoice_date: Date the invoice was issued.
        payable_by: Date when the invoice should be paid.
        vendor_name: Name of the vendor who created the invoice.
        vendor_address: Full address of the vendor.
        vendor_tax_id: Government tax ID of the vendor.
        remittance_address: Full address where the payment should be sent.
        subtotal: Subtotal of the invoice.
        total_discount: Total discount applied to the invoice.
        total_tax: Total tax applied to the invoice.
        invoice_total: Total charges associated with the invoice.
        payment_terms: Payment terms for the invoice.
        items: List of line items in the invoice.
        total_item_quantity: Total quantity of items in the invoice.
        items_customer_signature: Signature of the customer for the items in the invoice.
        items_vendor_signature: Signature of the vendor for the items in the invoice.
        returns: List of line items returned in the invoice.
        total_return_quantity: Total quantity of items returned in the invoice.
        returns_customer_signature: Signature of the customer for the returned items in the invoice.
        returns_vendor_signature: Signature of the vendor for the returned items in the invoice.
    """

    customer_name: Optional[str] = Field(
        description='Name of the customer being invoiced, e.g. Company A'
    )
    customer_address: Optional[InvoiceAddress] = Field(
        description='Full address of the customer, e.g. 123 Main St., City, Country'
    )
    customer_tax_id: Optional[str] = Field(
        description='Government tax ID of the customer, e.g. 123456789'
    )
    shipping_address: Optional[InvoiceAddress] = Field(
        description='Full address of the shipping location for the customer (null if the same as customer address), e.g. 123 Main St., City, Country'
    )
    purchase_order: Optional[str] = Field(
        description='Purchase order reference number, e.g. PO-1234'
    )
    invoice_id: Optional[str] = Field(
        description='Reference ID for the invoice (often invoice number), e.g. INV-1234'
    )
    invoice_date: Optional[str] = Field(
        description='Date the invoice was issued or delivered, e.g., 2021-01-01'
    )
    payable_by: Optional[str] = Field(
        description='Date when the invoice should be paid, e.g., 2021-01-15'
    )
    vendor_name: Optional[str] = Field(
        description='Name of the vendor who created the invoice, e.g. Company B'
    )
    vendor_address: Optional[InvoiceAddress] = Field(
        description='Full address of the vendor, e.g. 321 Main St., City, Country'
    )
    vendor_tax_id: Optional[str] = Field(
        description='Government tax ID of the vendor, e.g. 123456789'
    )
    remittance_address: Optional[InvoiceAddress] = Field(
        description='Full address where the payment should be sent (null if the same as vendor address), e.g. 321 Main St., City, Country'
    )
    subtotal: Optional[float] = Field(
        description='Subtotal of the invoice, e.g. 100.00'
    )
    total_discount: Optional[float] = Field(
        description='Total discount applied to the invoice, e.g. 10.00'
    )
    total_tax: Optional[float] = Field(
        description='Total tax applied to the invoice, e.g. 5.00'
    )
    invoice_total: Optional[float] = Field(
        description='Total charges associated with the invoice, e.g. 95.00'
    )
    payment_terms: Optional[str] = Field(
        description='Payment terms for the invoice, e.g. Net 90'
    )
    items: Optional[list[InvoiceItem]] = Field(
        description='List of line items in the invoice'
    )
    total_item_quantity: Optional[float] = Field(
        description='Total quantity of items in the invoice'
    )
    items_customer_signature: Optional[InvoiceSignature] = Field(
        description='Signature of the customer for the items in the invoice'
    )
    items_vendor_signature: Optional[InvoiceSignature] = Field(
        description='Signature of the vendor for the items in the invoice'
    )
    returns: Optional[list[InvoiceItem]] = Field(
        description='List of line items returned in the invoice'
    )
    total_return_quantity: Optional[float] = Field(
        description='Total quantity of items returned in the invoice'
    )
    returns_customer_signature: Optional[InvoiceSignature] = Field(
        description='Signature of the customer for the returned items in the invoice'
    )
    returns_vendor_signature: Optional[InvoiceSignature] = Field(
        description='Signature of the vendor for the returned items in the invoice'
    )

    @staticmethod
    def example():
        """
        Creates an empty example Invoice object.

        Returns:
            Invoice: An empty Invoice object.
        """

        return Invoice(
            customer_name='',
            customer_address=InvoiceAddress.example(),
            customer_tax_id='',
            shipping_address=InvoiceAddress.example(),
            purchase_order='',
            invoice_id='',
            invoice_date=datetime.now().strftime('%Y-%m-%d'),
            payable_by=datetime.now().strftime('%Y-%m-%d'),
            vendor_name='',
            vendor_address=InvoiceAddress.example(),
            vendor_tax_id='',
            remittance_address=InvoiceAddress.example(),
            subtotal=0.0,
            total_discount=0.0,
            total_tax=0.0,
            invoice_total=0.0,
            payment_terms='',
            items=[InvoiceItem.example()],
            total_item_quantity=0.0,
            items_customer_signature=InvoiceSignature.example(),
            items_vendor_signature=InvoiceSignature.example(),
            returns=[InvoiceItem.example()],
            total_return_quantity=0.0,
            returns_customer_signature=InvoiceSignature.example(),
            returns_vendor_signature=InvoiceSignature.example()
        )

    @staticmethod
    def from_json(json_str: str):
        """
        Creates an Invoice object from a JSON string.

        Args:
            json_str: The JSON string representing the Invoice object.

        Returns:
            Invoice: An Invoice object.
        """

        json_content = json.loads(json_str)

        def create_invoice_address(address):
            """
            Creates an InvoiceAddress object from a dictionary.

            Args:
                address: A dictionary representing an InvoiceAddress object.

            Returns:
                InvoiceAddress: An InvoiceAddress object.
            """

            if address is None:
                return None

            return InvoiceAddress(
                street=address.get('street', None),
                city=address.get('city', None),
                state=address.get('state', None),
                postal_code=address.get('postal_code', None),
                country=address.get('country', None)
            )

        def create_invoice_item(item):
            """
            Creates an InvoiceItem object from a dictionary.

            Args:
                product: A dictionary representing an InvoiceItem object.

            Returns:
                InvoiceItem: An InvoiceItem object.
            """

            if item is None:
                return None

            return InvoiceItem(
                product_code=item.get('product_code', None),
                description=item.get('description', None),
                quantity=item.get('quantity', None),
                tax=item.get('tax', None),
                tax_rate=item.get('tax_rate', None),
                unit_price=item.get('unit_price', None),
                total=item.get('total', None),
                reason=item.get('reason', None)
            )

        def create_invoice_signature(signature):
            """
            Creates an InvoiceSignature object from a dictionary.

            Args:
                signature: A dictionary representing an InvoiceSignature object.

            Returns:
                InvoiceSignature: An InvoiceSignature object.
            """

            if signature is None:
                return None

            return InvoiceSignature(
                signatory=signature.get('signatory', None),
                is_signed=signature.get('is_signed', None)
            )

        invoice_items = [create_invoice_item(
            product) for product in json_content.get('products', [])]
        invoice_returns = [create_invoice_item(
            return_product) for return_product in json_content.get('returns', [])]

        return Invoice(
            customer_name=json_content.get('customer_name', None),
            customer_address=create_invoice_address(
                json_content.get('customer_address', None)),
            customer_tax_id=json_content.get('customer_tax_id', None),
            shipping_address=create_invoice_address(
                json_content.get('shipping_address', None)),
            purchase_order=json_content.get('purchase_order', None),
            invoice_id=json_content.get('invoice_id', None),
            invoice_date=json_content.get('invoice_date', None),
            payable_by=json_content.get('payable_by', None),
            vendor_name=json_content.get('vendor_name', None),
            vendor_address=create_invoice_address(
                json_content.get('vendor_address', None)),
            vendor_tax_id=json_content.get('vendor_tax_id', None),
            remittance_address=create_invoice_address(
                json_content.get('remittance_address', None)),
            subtotal=json_content.get('subtotal', None),
            total_discount=json_content.get('total_discount', None),
            total_tax=json_content.get('total_tax', None),
            invoice_total=json_content.get('invoice_total', None),
            payment_terms=json_content.get('payment_terms', None),
            items=invoice_items,
            total_item_quantity=json_content.get('total_item_quantity', None),
            items_customer_signature=create_invoice_signature(
                json_content.get('items_customer_signature', None)),
            items_vendor_signature=create_invoice_signature(
                json_content.get('items_vendor_signature', None)),
            returns=invoice_returns,
            total_return_quantity=json_content.get(
                'total_return_quantity', None),
            returns_customer_signature=create_invoice_signature(
                json_content.get('returns_customer_signature', None)),
            returns_vendor_signature=create_invoice_signature(
                json_content.get('returns_vendor_signature', None))
        )

    def to_dict(self):
        """
        Converts the Invoice object to a dictionary.

        Returns:
            dict: The Invoice object as a dictionary.
        """

        def to_list(items, expected_type):
            return [item.to_dict() for item in items if isinstance(item, expected_type)]

        items = to_list(self.items or [], InvoiceItem)
        returns = to_list(self.returns or [], InvoiceItem)

        return {
            'customer_name': self.customer_name,
            'customer_address': self.customer_address.to_dict() if self.customer_address is not None else None,
            'customer_tax_id': self.customer_tax_id,
            'shipping_address': self.shipping_address.to_dict() if self.shipping_address is not None else None,
            'purchase_order': self.purchase_order,
            'invoice_id': self.invoice_id,
            'invoice_date': self.invoice_date,
            'payable_by': self.payable_by,
            'vendor_name': self.vendor_name,
            'vendor_address': self.vendor_address.to_dict() if self.vendor_address is not None else None,
            'vendor_tax_id': self.vendor_tax_id,
            'remittance_address': self.remittance_address.to_dict() if self.remittance_address is not None else None,
            'subtotal': self.subtotal,
            'total_discount': self.total_discount,
            'total_tax': self.total_tax,
            'invoice_total': self.invoice_total,
            'payment_terms': self.payment_terms,
            'products': items,
            'total_item_quantity': self.total_item_quantity,
            'items_customer_signature': self.items_customer_signature.to_dict() if self.items_customer_signature is not None else None,
            'items_vendor_signature': self.items_vendor_signature.to_dict() if self.items_vendor_signature is not None else None,
            'returns': returns,
            'total_return_quantity': self.total_return_quantity,
            'returns_customer_signature': self.returns_customer_signature.to_dict() if self.returns_customer_signature is not None else None,
            'returns_vendor_signature': self.returns_vendor_signature.to_dict() if self.returns_vendor_signature is not None else None
        }


class InvoiceEvaluator:
    """
    A class to evaluate the accuracy of an extracted invoice against its expected gold standard.

    Attributes:
        expected (Invoice): The expected invoice.
    """

    def __init__(self, expected: Invoice):
        """
        Initializes a new instance of the InvoiceEvaluator class.

        Args:
            expected: The expected invoice to compare against.
        """

        self.expected = expected

    def evaluate(self, actual: Optional[Invoice]):
        """
        Evaluates the accuracy of the extracted invoice against the expected invoice by comparing their attributes.

        Args:
            actual: The extracted invoice to evaluate.

        Returns:
            dict: A dictionary containing the accuracy of the extracted invoice by attribute.
        """

        def compare_address(expected: InvoiceAddress, actual: Optional[InvoiceAddress]):
            """
            Compares the accuracy of an expected address against an actual address including the overall accuracy.

            Args:
                expected: The expected address.
                actual: The actual address.

            Returns:
                dict: A dictionary containing the accuracy of the address by attribute.
            """

            accuracy = {
                'street': 0,
                'city': 0,
                'state': 0,
                'postal_code': 0,
                'country': 0,
                'overall': 0
            }

            if expected is None and actual is None:
                accuracy['overall'] = 1
                return accuracy

            if actual is None or expected is None:
                return accuracy

            accuracy['street'] = 1 if (expected.street or '').lower() == (
                actual.street or '').lower() else 0
            accuracy['city'] = 1 if (expected.city or '').lower() == (
                actual.city or '').lower() else 0
            accuracy['state'] = 1 if (expected.state or '').lower() == (
                actual.state or '').lower() else 0
            accuracy['postal_code'] = 1 if (expected.postal_code or '').lower() == (
                actual.postal_code or '').lower() else 0
            accuracy['country'] = 1 if (expected.country or '').lower() == (
                actual.country or '').lower() else 0

            accuracy['overall'] = (accuracy['street'] + accuracy['city'] + accuracy['state'] +
                                   accuracy['postal_code'] + accuracy['country']) / 5

            return accuracy

        def compare_item(expected: InvoiceItem, actual: Optional[InvoiceItem]):
            """
            Compares the accuracy of an expected line item against an actual line item including the overall accuracy.

            Args:
                expected: The expected line item.
                actual: The actual line item.

            Returns:
                dict: A dictionary containing the accuracy of the line item by attribute.
            """

            accuracy = {
                'product_code': 0,
                'description': 0,
                'quantity': 0,
                'tax': 0,
                'tax_rate': 0,
                'unit_price': 0,
                'total': 0,
                'reason': 0,
                'overall': 0
            }

            if expected is None and actual is None:
                accuracy['overall'] = 1
                return accuracy

            if actual is None or expected is None:
                return accuracy

            accuracy['product_code'] = 1 if (expected.product_code or '').lower() == (
                actual.product_code or '').lower() else 0
            accuracy['description'] = 1 if (expected.description or '').lower() == (
                actual.description or '').lower() else 0
            accuracy['quantity'] = 1 if expected.quantity == actual.quantity else 0
            accuracy['tax'] = 1 if expected.tax == actual.tax else 0
            accuracy['tax_rate'] = 1 if (expected.tax_rate or '').lower() == (
                actual.tax_rate or '').lower() else 0
            accuracy['unit_price'] = 1 if expected.unit_price == actual.unit_price else 0
            accuracy['total'] = 1 if expected.total == actual.total else 0
            accuracy['reason'] = 1 if (expected.reason or '').lower() == (
                actual.reason or '').lower() else 0

            accuracy['overall'] = (accuracy['product_code'] + accuracy['description'] + accuracy['quantity'] + accuracy['tax'] +
                                   accuracy['tax_rate'] + accuracy['unit_price'] + accuracy['total'] + accuracy['reason']) / 8

            return accuracy

        def compare_signature(expected: InvoiceSignature, actual: Optional[InvoiceSignature]):
            """
            Compares the accuracy of an expected signature against an actual signature including the overall accuracy.

            Args:
                expected: The expected signature.
                actual: The actual signature.

            Returns:
                dict: A dictionary containing the accuracy of the signature by attribute
            """

            accuracy = {
                'signatory': 0,
                'is_signed': 0,
                'overall': 0
            }

            if expected is None and actual is None:
                accuracy['overall'] = 1
                return accuracy

            if actual is None or expected is None:
                return accuracy

            accuracy['signatory'] = 1 if (expected.signatory or '').lower() == (
                actual.signatory or '').lower() else 0
            accuracy['is_signed'] = 1 if expected.is_signed == actual.is_signed else 0

            accuracy['overall'] = (
                accuracy['signatory'] + accuracy['is_signed']) / 2

            return accuracy

        accuracy = {
            'customer_name': 0,
            'customer_address': 0,
            'customer_tax_id': 0,
            'shipping_address': 0,
            'purchase_order': 0,
            'invoice_id': 0,
            'invoice_date': 0,
            'payable_by': 0,
            'vendor_name': 0,
            'vendor_address': 0,
            'vendor_tax_id': 0,
            'remittance_address': 0,
            'subtotal': 0,
            'total_discount': 0,
            'total_tax': 0,
            'invoice_total': 0,
            'payment_terms': 0,
            'items': [],
            'items_overall': 0,
            'total_item_quantity': 0,
            'items_customer_signature': 0,
            'items_vendor_signature': 0,
            'returns': [],
            'returns_overall': 0,
            'total_return_quantity': 0,
            'returns_customer_signature': 0,
            'returns_vendor_signature': 0,
            'overall': 0
        }

        if actual is None:
            return accuracy

        accuracy['customer_name'] = 1 if (self.expected.customer_name or '').lower(
        ) == (actual.customer_name or '').lower() else 0

        if actual.customer_address is None:
            accuracy['customer_address'] = {
                'overall': 1 if self.expected.customer_address is None else 0
            }
        else:
            accuracy['customer_address'] = compare_address(
                self.expected.customer_address, actual.customer_address)

        accuracy['customer_tax_id'] = 1 if (self.expected.customer_tax_id or '').lower(
        ) == (actual.customer_tax_id or '').lower() else 0

        if actual.shipping_address is None:
            accuracy['shipping_address'] = {
                'overall': 1 if self.expected.shipping_address is None else 0
            }
        else:
            accuracy['shipping_address'] = compare_address(
                self.expected.shipping_address, actual.shipping_address)

        accuracy['purchase_order'] = 1 if (self.expected.purchase_order or '').lower(
        ) == (actual.purchase_order or '').lower() else 0
        accuracy['invoice_id'] = 1 if (self.expected.invoice_id or '').lower(
        ) == (actual.invoice_id or '').lower() else 0
        accuracy['invoice_date'] = 1 if self.expected.invoice_date == actual.invoice_date else 0
        accuracy['payable_by'] = 1 if self.expected.payable_by == actual.payable_by else 0
        accuracy['vendor_name'] = 1 if (self.expected.vendor_name or '').lower(
        ) == (actual.vendor_name or '').lower() else 0

        if actual.vendor_address is None:
            accuracy['vendor_address'] = {
                'overall': 1 if self.expected.vendor_address is None else 0
            }
        else:
            accuracy['vendor_address'] = compare_address(
                self.expected.vendor_address, actual.vendor_address)

        accuracy['vendor_tax_id'] = 1 if (self.expected.vendor_tax_id or '').lower(
        ) == (actual.vendor_tax_id or '').lower() else 0

        if actual.remittance_address is None:
            accuracy['remittance_address'] = {
                'overall': 1 if self.expected.remittance_address is None else 0
            }
        else:
            accuracy['remittance_address'] = compare_address(
                self.expected.remittance_address, actual.remittance_address)

        accuracy['subtotal'] = 1 if self.expected.subtotal == actual.subtotal else 0
        accuracy['total_discount'] = 1 if self.expected.total_discount == actual.total_discount else 0
        accuracy['total_tax'] = 1 if self.expected.total_tax == actual.total_tax else 0
        accuracy['invoice_total'] = 1 if self.expected.invoice_total == actual.invoice_total else 0
        accuracy['payment_terms'] = 1 if (self.expected.payment_terms or '').lower(
        ) == (actual.payment_terms or '').lower() else 0

        if actual.items is None:
            accuracy['items_overall'] = 1 if self.expected.items is None else 0
        else:
            if self.expected.items is None:
                accuracy['items_overall'] = 0
            else:
                for actual_item in actual.items:
                    expected_item = next(
                        (item for item in self.expected.items if (item.product_code or '').lower() == (actual_item.product_code or '').lower()), None)
                    if expected_item is not None:
                        accuracy['items'].append(
                            compare_item(expected_item, actual_item))
                    else:
                        accuracy['items'].append({'overall': 0})

                num_items = len(accuracy['items']) if len(
                    accuracy['items']) > 0 else 1
                accuracy['items_overall'] = sum(
                    [product['overall'] for product in accuracy['items']]) / num_items

        accuracy['total_item_quantity'] = 1 if self.expected.total_item_quantity == actual.total_item_quantity else 0

        if actual.items_customer_signature is None:
            accuracy['items_customer_signature'] = {
                'overall': 1 if self.expected.items_customer_signature is None else 0
            }
        else:
            accuracy['items_customer_signature'] = compare_signature(
                self.expected.items_customer_signature, actual.items_customer_signature)

        if actual.items_vendor_signature is None:
            accuracy['items_vendor_signature'] = {
                'overall': 1 if self.expected.items_vendor_signature is None else 0
            }
        else:
            accuracy['items_vendor_signature'] = compare_signature(
                self.expected.items_vendor_signature, actual.items_vendor_signature)

        if actual.returns is None:
            accuracy['returns_overall'] = 1 if self.expected.returns is None else 0
        else:
            if self.expected.returns is None:
                accuracy['returns_overall'] = 0
            else:
                for actual_return in actual.returns:
                    expected_return = next(
                        (return_product for return_product in self.expected.returns if (return_product.product_code or '').lower() == (actual_return.product_code or '').lower()), None)
                    if expected_return is not None:
                        accuracy['returns'].append(
                            compare_item(expected_return, actual_return))
                    else:
                        accuracy['returns'].append({'overall': 0})

                num_returns = len(accuracy['returns']) if len(
                    accuracy['returns']) > 0 else 1
                accuracy['returns_overall'] = sum(
                    [return_product['overall'] for return_product in accuracy['returns']]) / num_returns

        accuracy['total_return_quantity'] = 1 if self.expected.total_return_quantity == actual.total_return_quantity else 0

        if actual.returns_customer_signature is None:
            accuracy['returns_customer_signature'] = {
                'overall': 1 if self.expected.returns_customer_signature is None else 0
            }
        else:
            accuracy['returns_customer_signature'] = compare_signature(
                self.expected.returns_customer_signature, actual.returns_customer_signature)

        if actual.returns_vendor_signature is None:
            accuracy['returns_vendor_signature'] = {
                'overall': 1 if self.expected.returns_vendor_signature is None else 0
            }
        else:
            accuracy['returns_vendor_signature'] = compare_signature(
                self.expected.returns_vendor_signature, actual.returns_vendor_signature)

        accuracy['overall'] = (accuracy['customer_name'] + accuracy['customer_address']['overall'] + accuracy['customer_tax_id'] + accuracy['shipping_address']['overall'] +
                               accuracy['purchase_order'] + accuracy['invoice_id'] + accuracy['invoice_date'] + accuracy['payable_by'] + accuracy['vendor_name'] +
                               accuracy['vendor_address']['overall'] + accuracy['vendor_tax_id'] + accuracy['remittance_address']['overall'] + accuracy['subtotal'] +
                               accuracy['total_discount'] + accuracy['total_tax'] + accuracy['invoice_total'] + accuracy['payment_terms'] + accuracy['items_overall'] +
                               accuracy['total_item_quantity'] + accuracy['items_customer_signature']['overall'] + accuracy['items_vendor_signature']['overall'] +
                               accuracy['returns_overall'] + accuracy['total_return_quantity'] + accuracy['returns_customer_signature']['overall'] + accuracy['returns_vendor_signature']['overall']) / 25

        return accuracy
