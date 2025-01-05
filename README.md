# Starcraft Data Platform

## **Status: Work in Progress [![Coverage Status](https://coveralls.io/repos/github/username/repo/badge.svg?branch=main)](https://coveralls.io/github/username/repo?branch=main) **


This repository is under active development. It defines the database architecture for ingesting, storing, and analyzing Starcraft II replay data.

---

## **Overview**

The **Starcraft Data Platform** is designed to:
- Store raw replay data, player information, and event logs in a relational database.
- Provide analytics views and materialized tables for advanced insights.
- Enable machine learning workflows by supporting feature engineering and model outputs.

---

## **Planned Features**

1. **Core Functionality**:
   - Relational database schema for storing raw replay data.
   - Analytics views for player statistics and performance trends.
   - ML schema for storing model outputs and feature sets.

2. **Technology Stack**:
   - PostgreSQL for database storage.
   - SQLAlchemy for ORM models.
   - Docker for containerized deployment.

3. **Future Enhancements**:
   - Performance optimization for materialized views.
   - Expanded analytics for build orders and map-specific trends.

---

## **Current Focus**

The current phase of development is focused on:
- Designing the `raw` schema for replay ingestion.
- Creating analytics views for player statistics.

---

## **Getting Started**

⚠️ **This project is not yet ready for deployment or public use.** Setup instructions will be added as development progresses.

---

## **Planned Structure**

This repository will be organized into the following structure:

- **`db/`**: Contains all database-related files.
  - **`schema.sql`**: A consolidated SQL file for creating all database schemas, including raw, analytics, and ML schemas.
  - **`models/`**: A directory housing SQLAlchemy ORM models.
    - **`replay.py`**: ORM models for replay metadata tables (e.g., Info, Player, Team).
    - **`events.py`**: ORM models for event data (e.g., UnitBornEvent, SelectionEvent).
    - **`datapack.py`**: ORM models for unit and ability metadata (e.g., UnitType, Ability).
  - **`analytics/`**: SQL files for analytics views and materialized tables.
    - **`player_stats.sql`**: A view aggregating player performance metrics.
    - **`map_performance.sql`**: A view tracking win rates by map and race.
    - **`player_stats_summary.sql`**: A materialized view summarizing player statistics across replays.

- **`tests/`**: Contains unit tests for validating schema and models.
  - **`test_schema.py`**: Tests to ensure the database schema is correctly defined.
  - **`test_models.py`**: Tests for ORM models to verify accurate data interaction.
  - **`test_analytics.py`**: Tests for analytics queries and performance.

- **`Dockerfile`**: Configuration for containerizing the project, ensuring consistent environments for development and deployment.

- **`README.md`**: This documentation file, providing an overview of the project and its structure.

---

## **How to Contribute**

Contributions are welcome once the repository reaches a stable state. If you'd like to collaborate, please reach out or open an issue to discuss ideas.

---

## **License**

[MIT License]

---
