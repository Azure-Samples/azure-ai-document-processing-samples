from __future__ import annotations
from datetime import datetime
import json
from typing import Optional
from pydantic import BaseModel, Field


class InvoiceSignature(BaseModel):
    """
    A class representing a signature for an invoice.

    Attributes:
        type: Type of signature.
        name: Name of the person who signed the invoice.
        is_signed: Indicates if the invoice is signed.
    """

    type: Optional[str] = Field(
        description='Type of signature, e.g., Recipient, Customer, Driver'
    )
    name: Optional[str] = Field(
        description='Name of the person who signed the invoice'
    )
    is_signed: Optional[bool] = Field(
        description='Indicates if the invoice is signed'
    )

    @staticmethod
    def example(type=''):
        """
        Creates an empty example InvoiceSignature object.

        Args:
            type: The type of the signature.

        Returns:
            InvoiceSignature: An empty InvoiceSignature object
        """
        return InvoiceSignature(
            type=type,
            name='',
            is_signed=False
        )

    def to_dict(self):
        """
        Converts the InvoiceSignature object to a dictionary.

        Returns:
            dict: The InvoiceSignature object as a dictionary.
        """

        return {
            'type': self.type,
            'name': self.name,
            'is_signed': self.is_signed
        }


class InvoiceProduct(BaseModel):
    """
    A class representing a product item in an invoice.

    Attributes:
        id: Identifier of the product.
        description: Description of the product.
        unit_price: Unit price of the product.
        quantity: Quantity of the product.
        total: Total price of the product.
        reason: Reason for returning the product.
    """

    id: Optional[str] = Field(
        description='Identifier of the product'
    )
    description: Optional[str] = Field(
        description='Description of the product',
    )
    unit_price: Optional[float] = Field(
        description='Unit price of the product'
    )
    quantity: Optional[int] = Field(
        description='Quantity of the product'
    )
    total: Optional[float] = Field(
        description='Total price of the product'
    )
    reason: Optional[str] = Field(
        description='Reason for returning the product'
    )

    @staticmethod
    def example():
        """
        Creates an empty example InvoiceProduct object.

        Returns:
            InvoiceProduct: An empty InvoiceProduct object.
        """
        return InvoiceProduct(
            id='',
            description='',
            unit_price=0.0,
            quantity=0.0,
            total=0.0,
            reason=''
        )

    def to_dict(self):
        """
        Converts the InvoiceProduct object to a dictionary.

        Returns:
            dict: The InvoiceProduct object as a dictionary.
        """

        return {
            'id': self.id,
            'description': self.description,
            'unit_price': self.unit_price,
            'quantity': self.quantity,
            'total': self.total,
            'reason': self.reason
        }


class Invoice(BaseModel):
    """
    A class representing an invoice.

    Attributes:
        invoice_number: Invoice number.
        purchase_order_number: Purchase order number.
        customer_name: Name of the customer/company.
        customer_address: Full address of the customer/company.
        delivery_date: Date of delivery.
        payable_by: Date when the invoice should be paid.
        products: List of products in the invoice.
        returns: List of products returned in the invoice.
        total_product_quantity: Total quantity of products in the invoice.
        total_product_price: Total price of products in the invoice.
        product_signatures: List of signatures for the products in the invoice.
        returns_signatures: List of signatures for the returned products in the invoice.
    """

    invoice_number: Optional[str] = Field(
        description='Invoice number'
    )
    purchase_order_number: Optional[str] = Field(
        description='Purchase order number'
    )
    customer_name: Optional[str] = Field(
        description='Name of the customer/company, e.g. Company A'
    )
    customer_address: Optional[str] = Field(
        description='Full address of the customer/company, e.g. 123 Main St., City, Country'
    )
    delivery_date: Optional[str] = Field(
        description='Date of delivery, e.g., 2021-01-01'
    )
    payable_by: Optional[str] = Field(
        description='Date when the invoice should be paid, e.g., 2021-01-15'
    )
    products: Optional[list[InvoiceProduct]] = Field(
        description='List of products in the invoice'
    )
    returns: Optional[list[InvoiceProduct]] = Field(
        description='List of products returned in the invoice'
    )
    total_product_quantity: Optional[float] = Field(
        description='Total quantity of products in the invoice'
    )
    total_product_price: Optional[float] = Field(
        description='Total price of products in the invoice'
    )
    product_signatures: Optional[list[InvoiceSignature]] = Field(
        description='List of signatures for the products in the invoice'
    )
    returns_signatures: Optional[list[InvoiceSignature]] = Field(
        description='List of signatures for the returned products in the invoice'
    )

    @staticmethod
    def example():
        """
        Creates an empty example Invoice object.

        Returns:
            Invoice: An empty Invoice object.
        """

        return Invoice(
            invoice_number='',
            purchase_order_number='',
            customer_name='',
            customer_address='',
            delivery_date=datetime.now().strftime('%Y-%m-%d'),
            payable_by=datetime.now().strftime('%Y-%m-%d'),
            products=[InvoiceProduct.example()],
            returns=[InvoiceProduct.example()],
            total_product_quantity=0.0,
            total_product_price=0.0,
            product_signatures=[
                InvoiceSignature.example('Customer'),
                InvoiceSignature.example('Driver')
            ],
            returns_signatures=[InvoiceSignature.example()]
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

        def create_invoice_product(product):
            """
            Creates an InvoiceProduct object from a dictionary.

            Args:
                product: A dictionary representing an InvoiceProduct object.

            Returns:
                InvoiceProduct: An InvoiceProduct object.
            """

            return InvoiceProduct(
                id=product.get('id', None),
                description=product.get('description', None),
                unit_price=product.get('unit_price', None),
                quantity=product.get('quantity', None),
                total=product.get('total', None),
                reason=product.get('reason', None)
            )

        def create_invoice_signature(signature):
            """
            Creates an InvoiceSignature object from a dictionary.

            Args:
                signature: A dictionary representing an InvoiceSignature object.

            Returns:
                InvoiceSignature: An InvoiceSignature object.
            """

            return InvoiceSignature(
                type=signature.get('type', None),
                name=signature.get('name', None),
                is_signed=signature.get('is_signed', None)
            )

        invoice_products = [create_invoice_product(
            product) for product in json_content.get('products', [])]
        invoice_returns = [create_invoice_product(
            return_product) for return_product in json_content.get('returns', [])]
        invoice_product_signatures = [create_invoice_signature(
            signature) for signature in json_content.get('product_signatures', [])]
        invoice_return_signatures = [create_invoice_signature(
            signature) for signature in json_content.get('returns_signatures', [])]

        return Invoice(
            invoice_number=json_content.get('invoice_number', None),
            purchase_order_number=json_content.get(
                'purchase_order_number', None),
            customer_name=json_content.get('customer_name', None),
            customer_address=json_content.get('customer_address', None),
            delivery_date=json_content.get('delivery_date', None),
            payable_by=json_content.get('payable_by', None),
            products=invoice_products,
            returns=invoice_returns,
            total_product_quantity=json_content.get(
                'total_product_quantity', None),
            total_product_price=json_content.get('total_product_price', None),
            product_signatures=invoice_product_signatures,
            returns_signatures=invoice_return_signatures
        )

    def to_dict(self):
        """
        Converts the Invoice object to a dictionary.

        Returns:
            dict: The Invoice object as a dictionary.
        """

        def to_list(items, expected_type):
            return [item.to_dict() for item in items if isinstance(item, expected_type)]

        products = to_list(self.products or [], InvoiceProduct)
        returns = to_list(self.returns or [], InvoiceProduct)
        product_signatures = to_list(
            self.product_signatures or [], InvoiceSignature)
        return_signatures = to_list(
            self.returns_signatures or [], InvoiceSignature)

        return {
            'invoice_number': self.invoice_number,
            'purchase_order_number': self.purchase_order_number,
            'customer_name': self.customer_name,
            'customer_address': self.customer_address,
            'delivery_date': self.delivery_date,
            'payable_by': self.payable_by,
            'products': products,
            'returns': returns,
            'total_product_quantity': self.total_product_quantity,
            'total_product_price': self.total_product_price,
            'product_signatures': product_signatures,
            'returns_signatures': return_signatures
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

        def compare_product(expected_product: InvoiceProduct, actual_product: Optional[InvoiceProduct]):
            """
            Compares the accuracy of an expected product against an actual product including the overall accuracy.

            Args:
                expected_product: The expected product.
                actual_product: The actual product.

            Returns:
                dict: A dictionary containing the accuracy of the product by attribute.
            """

            product_accuracy = {
                'id': 0,
                'description': 0,
                'unit_price': 0,
                'quantity': 0,
                'total': 0,
                'reason': 0,
                'overall': 0
            }

            if actual_product is None:
                return product_accuracy

            product_accuracy['id'] = 1 if (expected_product.id or '').lower() == (
                actual_product.id or '').lower() else 0
            product_accuracy['description'] = 1 if (expected_product.description or '').lower(
            ) == (actual_product.description or '').lower() else 0
            product_accuracy['unit_price'] = 1 if expected_product.unit_price == actual_product.unit_price else 0
            product_accuracy['quantity'] = 1 if expected_product.quantity == actual_product.quantity else 0
            product_accuracy['total'] = 1 if expected_product.total == actual_product.total else 0
            product_accuracy['reason'] = 1 if (expected_product.reason or '').lower() == (
                actual_product.reason or '').lower() else 0
            product_accuracy['overall'] = (product_accuracy['id'] + product_accuracy['description'] + product_accuracy['unit_price'] +
                                           product_accuracy['quantity'] + product_accuracy['total'] + product_accuracy['reason']) / 6

            return product_accuracy

        def compare_signature(expected_signature: InvoiceSignature, actual_signature: Optional[InvoiceSignature]):
            """
            Compares the accuracy of an expected signature against an actual signature including the overall accuracy.

            Args:
                expected_signature: The expected signature.
                actual_signature: The actual signature.

            Returns:
                dict: A dictionary containing the accuracy of the signature by attribute
            """

            signature_accuracy = {
                'type': 0,
                'name': 0,
                'is_signed': 0,
                'overall': 0
            }

            if actual_signature is None:
                return signature_accuracy

            signature_accuracy['type'] = 1 if (expected_signature.type or '').lower() == (
                actual_signature.type or '').lower() else 0
            signature_accuracy['name'] = 1 if (expected_signature.name or '').lower() == (
                actual_signature.name or '').lower() else 0
            signature_accuracy['is_signed'] = 1 if expected_signature.is_signed == actual_signature.is_signed else 0
            signature_accuracy['overall'] = (
                signature_accuracy['type'] + signature_accuracy['name'] + signature_accuracy['is_signed']) / 3

            return signature_accuracy

        invoice_accuracy = {
            'invoice_number': 0,
            'purchase_order_number': 0,
            'customer_name': 0,
            'customer_address': 0,
            'delivery_date': 0,
            'payable_by': 0,
            'products': [],
            'products_overall': 0,
            'returns': [],
            'returns_overall': 0,
            'total_product_quantity': 0,
            'total_product_price': 0,
            'product_signatures': [],
            'product_signatures_overall': 0,
            'returns_signatures': [],
            'returns_signatures_overall': 0,
            'overall': 0
        }

        if actual is None:
            return invoice_accuracy

        invoice_accuracy['invoice_number'] = 1 if (self.expected.invoice_number or '').lower(
        ) == (actual.invoice_number or '').lower() else 0
        invoice_accuracy['purchase_order_number'] = 1 if (self.expected.purchase_order_number or '').lower(
        ) == (actual.purchase_order_number or '').lower() else 0
        invoice_accuracy['customer_name'] = 1 if (self.expected.customer_name or '').lower(
        ) == (actual.customer_name or '').lower() else 0
        invoice_accuracy['customer_address'] = 1 if (self.expected.customer_address or '').lower(
        ) == (actual.customer_address or '').lower() else 0
        invoice_accuracy['delivery_date'] = 1 if self.expected.delivery_date == actual.delivery_date else 0
        invoice_accuracy['payable_by'] = 1 if self.expected.payable_by == actual.payable_by else 0
        invoice_accuracy['total_product_quantity'] = 1 if self.expected.total_product_quantity == actual.total_product_quantity else 0
        invoice_accuracy['total_product_price'] = 1 if self.expected.total_product_price == actual.total_product_price else 0

        if actual.products is None:
            invoice_accuracy['products_overall'] = 1 if self.expected.products is None else 0
        else:
            if self.expected.products is None:
                invoice_accuracy['products_overall'] = 0
            else:
                for actual_product in actual.products:
                    expected_product = next(
                        (product for product in self.expected.products if (product.id or '').lower() == (actual_product.id or '').lower()), None)
                    if expected_product is not None:
                        invoice_accuracy['products'].append(
                            compare_product(expected_product, actual_product))
                    else:
                        invoice_accuracy['products'].append({'overall': 0})

                num_products = len(invoice_accuracy['products']) if len(
                    invoice_accuracy['products']) > 0 else 1
                invoice_accuracy['products_overall'] = sum(
                    [product['overall'] for product in invoice_accuracy['products']]) / num_products

        if actual.returns is None:
            invoice_accuracy['returns_overall'] = 1 if self.expected.returns is None else 0
        else:
            if self.expected.returns is None:
                invoice_accuracy['returns_overall'] = 0
            else:
                for actual_return in actual.returns:
                    expected_return = next(
                        (return_product for return_product in self.expected.returns if (return_product.id or '').lower() == (actual_return.id or '').lower()), None)
                    if expected_return is not None:
                        invoice_accuracy['returns'].append(
                            compare_product(expected_return, actual_return))
                    else:
                        invoice_accuracy['returns'].append({'overall': 0})

                num_returns = len(invoice_accuracy['returns']) if len(
                    invoice_accuracy['returns']) > 0 else 1
                invoice_accuracy['returns_overall'] = sum(
                    [return_product['overall'] for return_product in invoice_accuracy['returns']]) / num_returns

        if actual.product_signatures is None:
            invoice_accuracy['product_signatures_overall'] = 1 if self.expected.product_signatures is None else 0
        else:
            if self.expected.product_signatures is None:
                invoice_accuracy['product_signatures_overall'] = 0
            else:
                for actual_product_signature in actual.product_signatures:
                    expected_product_signature = next(
                        (product_signature for product_signature in self.expected.product_signatures if (product_signature.type or '').lower() == (actual_product_signature.type or '').lower()), None)
                    if expected_product_signature is not None:
                        invoice_accuracy['product_signatures'].append(
                            compare_signature(expected_product_signature, actual_product_signature))
                    else:
                        invoice_accuracy['product_signatures'].append(
                            {'overall': 0})

                num_product_signatures = len(invoice_accuracy['product_signatures']) if len(
                    invoice_accuracy['product_signatures']) > 0 else 1
                invoice_accuracy['product_signatures_overall'] = sum(
                    [product_signature['overall'] for product_signature in invoice_accuracy['product_signatures']]) / num_product_signatures

        if actual.returns_signatures is None:
            invoice_accuracy['returns_signatures_overall'] = 1 if self.expected.returns_signatures is None else 0
        else:
            if self.expected.returns_signatures is None:
                invoice_accuracy['returns_signatures_overall'] = 0
            else:
                for actual_return_signature in actual.returns_signatures:
                    expected_return_signature = next(
                        (return_signature for return_signature in self.expected.returns_signatures if (return_signature.type or '').lower() == (actual_return_signature.type or '').lower()), None)
                    if expected_return_signature is not None:
                        invoice_accuracy['returns_signatures'].append(
                            compare_signature(expected_return_signature, actual_return_signature))
                    else:
                        invoice_accuracy['returns_signatures'].append(
                            {'overall': 0})

                num_return_signatures = len(invoice_accuracy['returns_signatures']) if len(
                    invoice_accuracy['returns_signatures']) > 0 else 1
                invoice_accuracy['returns_signatures_overall'] = sum(
                    [return_signature['overall'] for return_signature in invoice_accuracy['returns_signatures']]) / num_return_signatures

        invoice_accuracy['overall'] = (invoice_accuracy['invoice_number'] + invoice_accuracy['purchase_order_number'] + invoice_accuracy['customer_name'] + invoice_accuracy['customer_address'] +
                                       invoice_accuracy['delivery_date'] + invoice_accuracy['payable_by'] + invoice_accuracy['total_product_quantity'] + invoice_accuracy['total_product_price'] +
                                       invoice_accuracy['products_overall'] + invoice_accuracy['returns_overall'] + invoice_accuracy['product_signatures_overall'] + invoice_accuracy['returns_signatures_overall']) / 12

        return invoice_accuracy
