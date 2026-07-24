# Project Forge - AI Engineering Guide

Version: 0.0.1

Status: Active

---

## Mission

Project Forge is an AI-powered Game Development Operating System.

Its purpose is to automate and orchestrate every stage of professional game development.

Forge does not simply generate assets.

Forge manages an entire production pipeline.

---

## Engineering Principles

1. Clean Architecture

2. Modular Design

3. Single Responsibility

4. Documentation First

5. Automation Before Manual Work

6. Test Before Release

7. Every Sprint must produce a working version.

---

## Coding Standards

- Small modules
- Readable code
- No duplicated logic
- Type hints whenever possible
- Clear naming
- No magic numbers
- Configuration separated from code

---

## Folder Responsibilities

app/core

Business logic.

Never depends on UI.

---

app/services

Services.

External integrations.

AI providers.

Filesystem.

Database.

---

app/ui

Desktop interface.

Only visual components.

---

app/models

Application models.

DTOs.

Entities.

---

app/utils

Utilities.

Helpers.

Shared code.

---

app/config

Configuration.

Settings.

Constants.

---

## Documentation Rules

Every new feature must update:

README

ROADMAP

CHANGELOG

Architecture (if necessary)

---

## Commit Convention

feat:

new feature

fix:

bug fix

refactor:

internal improvement

docs:

documentation

test:

tests

---

## AI Rules

Never delete existing functionality.

Never rename folders without updating references.

Never generate temporary code.

Always prefer maintainability over cleverness.

Always document important architectural decisions.

---

## Goal

Project Forge must become the definitive operating system for AI-assisted game development.