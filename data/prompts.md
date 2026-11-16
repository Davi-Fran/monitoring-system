# Prompts utilizados para gerar os dados de população

Ferramenta de IA: Claude Opus 5.5

## Prompt
```
Sendo assim, poderia gerar os dados nos CSVs e em um arquivo SQL por favor? Somente lembrando, os dados podem ser o mesmo (resalvas às questões de senha no SQL)
```

## Contexto fornecido à IA (na mesma conversa, antes do prompt)

- Enunciado do Projeto Integrador (PDF);
- DER final do projeto, com as tabelas `app_laboratory`, `app_micro_controller_model`, `app_micro_controller`, `app_sensor_model`, `app_sensor`, `app_sensor_reading` e `app_user`;

- Regras definidas na modelagem:
  - `sm_function` (TextChoices): `temperature`, `humidity`, `luminosity`, `count`;
  - `sm_measurement_unit` (TextChoices), definida pela função: `°C`, `%`, `lux`, `un`;
  - MAC no formato `XX:XX:XX:XX:XX:XX` (maiúsculas, separado por `:`), único;
  - `lab_name` com no máximo 20 caracteres;
  - leituras com data no passado; umidade entre 0 e 100; luminosidade e contagem não negativas; contagem inteira;
- Os dados do CSV e do SQL são os mesmos (o professor escolhe um dos dois para popular o banco).
- No SQL, as senhas precisam ser hashes válidos do Django (não texto puro).
- Usuários: 
  - Superusuário:`lin`/`123`;
  - Admin: `senai_admin`/`123456`;
  - Comum: `senai`/`123456`;