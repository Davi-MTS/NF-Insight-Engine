# Data Model — FISCALIS

## 1. Table: notas_fiscais

| Field             | Type        | Description                    |
|------------------|------------|--------------------------------|
| chave_acesso     | String(44) | Unique fiscal identifier       |
| url              | String     | Invoice consultation URL       |
| data_hora_leitura| Timestamp  | Moment of QR ingestion         |

---

## 2. Table: notas_detalhes

| Field             | Type      | Description                    |
|------------------|----------|--------------------------------|
| chave_acesso     | String   | Foreign key reference          |
| data_hora_venda  | Timestamp| Sale timestamp                 |
| forma_pagamento  | String   | Payment method                 |
| total_venda      | Float    | Total sale value               |

---

## 3. Table: itens_nota

| Field         | Type    | Description                |
|--------------|--------|----------------------------|
| chave_acesso | String | Invoice foreign key        |
| produto      | String | Product name               |
| quantidade   | Float  | Quantity purchased         |
| preco_unitario| Float | Unit price                 |
| total_item   | Float  | Total item value           |
