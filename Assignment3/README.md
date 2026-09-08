# CampusEats — Tutorial 3 / Assignment 3

## External SOAP Partner

**Partner:** CampusPay External Payment Services  
**Operation:** `charge`

### Team
- Anurag Sharma — Leader
- Mohit Tailor
- Harshita Rathore
- Harendra Godara

### Submission Files
- `integration.pdf`
- `partner.wsdl`
- `soap-request.xml`
- `soap-response.xml`
- `soap-fault.xml`

### SOAP Flow
```text
CampusEats placeOrder
      ↓
Payment Adapter
      ↓ SOAP charge
External Payment Gateway
      ↓
approved / SOAP Fault
      ↓
CampusEats payment result
```

### HTTP
`POST /soap/PaymentGateway`

`SOAPAction: "http://campuseats.example.com/payment/charge"`

### Discovery Registry
```text
business:  CampusPay External Payment Services
service:   CampusEats Payment Gateway
endpoint:  https://payments.partner.example.com/soap/PaymentGateway
WSDL:      https://payments.partner.example.com/wsdl/PaymentGateway.wsdl
operation: charge
```

### Fault Mapping
`card_declined` → `placeOrder → payment declined`

The external partner's vocabulary is kept inside the integration layer and is not exposed to students.
