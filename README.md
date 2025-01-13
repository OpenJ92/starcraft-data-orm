## Status: Work in Progress [![Coverage Status](https://coveralls.io/repos/github/OpenJ92/starcraft-data-orm/badge.svg?branch=main)](https://coveralls.io/github/OpenJ92/starcraft-data-orm?branch=main)

## Starcraft Data ORM
**Starcraft Data ORM** is a foundational library of SQLAlchemy-based ORM models for Starcraft replay data. It provides database sessions for each schema, enabling seamless integration with the broader Starcraft Data Platform and its components.

### Features
- **Replay Data Models:** Define and manage key replay-related entities, including players, units, events, and game metadata.
- **Schema-Specific Sessions:** Includes [`SessionLocal`](https://github.com/OpenJ92/starcraft-data-orm/blob/main/starcraft_data_orm/warehouse/config.py) in [`starcraft/warehouse/config.py`](https://github.com/OpenJ92/starcraft-data-orm/blob/main/starcraft_data_orm/warehouse/config.py) for efficient database interactions.
- **SQLAlchemy Base Objects:** Supplies prebuilt Base objects for use with [`injection-manager`](https://github.com/OpenJ92/injection-manager) objects, enabling seamless data injection workflows.
- **Integration Ready:** Works seamlessly with [`starcraft-injection-manager`](https://github.com/OpenJ92/starcraft-injection-manager) and [`starcraft-gather-manager`](https://github.com/OpenJ92/starcraft-gather-manager) for pipeline workflows.
- **Scalable Design:** Supports extensions to accommodate evolving analytics and machine learning requirements.
- **Async Compatibility:** Built to handle modern async frameworks and workflows.

### Installation
```bash
pip install starcraft-data-orm
```

### Usage
Setting Up the ORM
``` python
Copy code
from starcraft.warehouse.config import SessionLocal, SyncSessionLocal
from starcraft_data_orm.warehouse.info import info

# Use the appropriate session for async or sync workflows
async_session = SessionLocal()
sync_session = SyncSessionLocal()

# Example with SyncSessionLocal
with sync_session() as session:
    result = session.query(info).first()
    print(f"Info: {result}")
```

### Session Management
The SessionLocal and SyncSessionLocal sessions are preconfigured to handle database interactions specific to the Starcraft warehouse schema.

### Development Status
This project is under active development. While stable for core functionality, additional models and features are being added.

### Contributing
Contributions are welcome! Please open an issue or submit a pull request if you would like to add new features or report bugs.

### License
This project is licensed under the MIT License. See the LICENSE file for details.
