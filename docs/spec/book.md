cat > docs/spec/book.md << 'EOF'
# Aura Analytics — Spec Book

## 1. Vision & Goals
- Unify "Spec → Contract → Tests" per agent.

## 2. Contracts
- JSON Schemas: insight, hypothesis, report.

## 3. Validation
- ajv-cli@5, draft2020-12, allowUnionTypes.

## 4. MVP Flow
- Upload → Agents → Validator → Report (MD/HTML/PDF).
