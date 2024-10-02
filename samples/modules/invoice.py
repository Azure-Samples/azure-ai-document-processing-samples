from __future__ import annotations
from datetime import datetime
import json
from typing import Optional
from pydantic import BaseModel


class InvoiceSignature(BaseModel):
    type: Optional[str]
    name: Optional[str]
    is_signed: Optional[bool]

    @staticmethod
    def empty(type=''):
        return InvoiceSignature(
            type=type,
            name='',
            is_signed=False
        )

    def to_dict(self):
        return {
            'type': self.type,
            'name': self.name,
            'is_signed': self.is_signed
        }


class InvoiceProduct(BaseModel):
    id: Optional[str]
    description: Optional[str]
    unit_price: Optional[float]
    quantity: Optional[float]
    total: Optional[float]
    reason: Optional[str]

    @staticmethod
    def empty():
        return InvoiceProduct(
            id='',
            description='',
            unit_price=0.0,
            quantity=0.0,
            total=0.0,
            reason=''
        )

    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'unit_price': self.unit_price,
            'quantity': self.quantity,
            'total': self.total,
            'reason': self.reason
        }


class Invoice(BaseModel):
    invoice_number: Optional[str]
    purchase_order_number: Optional[str]
    customer_name: Optional[str]
    customer_address: Optional[str]
    delivery_date: Optional[str]
    payable_by: Optional[str]
    products: Optional[list[InvoiceProduct]]
    returns: Optional[list[InvoiceProduct]]
    total_product_quantity: Optional[float]
    total_product_price: Optional[float]
    product_signatures: Optional[list[InvoiceSignature]]
    returns_signatures: Optional[list[InvoiceSignature]]

    @staticmethod
    def empty():
        return Invoice(
            invoice_number='',
            purchase_order_number='',
            customer_name='',
            customer_address='',
            delivery_date=datetime.now().strftime('%Y-%m-%d'),
            payable_by=datetime.now().strftime('%Y-%m-%d'),
            products=[InvoiceProduct.empty()],
            returns=[InvoiceProduct.empty()],
            total_product_quantity=0.0,
            total_product_price=0.0,
            product_signatures=[
                InvoiceSignature.empty('Customer'),
                InvoiceSignature.empty('Driver')
            ],
            returns_signatures=[InvoiceSignature.empty()]
        )

    @staticmethod
    def empty_json():
        return json.dumps(Invoice.empty().to_dict())

    def to_dict(self):
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
    def __init__(self, expected: Invoice):
        self.expected = expected

    def evaluate(self, actual: Optional[Invoice]):
        def compare_product(expected_product: InvoiceProduct, actual_product: Optional[InvoiceProduct]):
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
