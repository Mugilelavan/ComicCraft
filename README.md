# ComicCraft

ComicCraft is an AI-powered 5-panel comic creator.

## Architecture

User
↓
FastAPI
↓
Gemini Outline
↓
Gemini Story
↓
Image Generation
↓
Layout Builder
↓
PDF Export
↓
Comic Preview

## Windows Setup

Open PowerShell in the ComicCraft folder.

### 1. Create virtual environment

```powershell
py -3.11 -m venv env