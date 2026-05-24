# ⚛️ Frontend - AI Policy Analyzer

<div align="center">

[![React](https://img.shields.io/badge/React-18+-61dafb?style=for-the-badge&logo=react&logoColor=black)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Vite-5.0+-646cff?style=for-the-badge&logo=vite&logoColor=white)](https://vitejs.dev/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.3+-06b6d4?style=for-the-badge&logo=tailwindcss&logoColor=white)](https://tailwindcss.com/)
[![Node.js](https://img.shields.io/badge/Node.js-16+-339933?style=for-the-badge&logo=node.js&logoColor=white)](https://nodejs.org/)

**Modern, responsive React frontend with real-time streaming chat and policy analysis**

[🚀 Quick Start](#quick-start) • [🏗️ Architecture](#architecture) • [🎨 Components](#components) • [🎯 Styling](#styling)

</div>

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Navigate to frontend directory
cd frontend

# Install Node dependencies
npm install
```

### 2. Configure API URL

Create a `.env` file in the frontend directory:

```bash
# For local development
echo 'VITE_API_URL=http://127.0.0.1:8001' > .env

# Or for production
# VITE_API_URL=https://your-railway-backend.railway.app
```

### 3. Start Development Server

```bash
# Start Vite dev server with hot reload
npm run dev
```

The app will open at: **http://localhost:5173**

### 4. Build for Production

```bash
# Create optimized production build
npm run build

# Preview production build locally
npm run preview
```

---

## 🏗️ Architecture

### Component Hierarchy

```
App.jsx (Main Router)
├── Sidebar
│   ├── Mode Toggle (Chat / Evaluator)
│   └── Navigation
│
├── ChatWindow (Mode: Chat)
│   ├── Message[] (Assistant & User messages)
│   ├── SourcesPanel (for each message)
│   └── Input Form
│
└── PolicyEvaluator (Mode: Evaluator)
    ├── Form (Policy textarea)
    ├── Structured Analysis Sections
    ├── SourcesPanel
    └── Result Cards
```

### Data Flow

```
User Input
    ▼
Event Handler (handleSubmit)
    ▼
apiClient.chat() or apiClient.evaluatePolicy()
    ▼
Fetch (with streaming for chat)
    ▼
Process Response Stream
    ▼
Update State (setMessages, setEvaluation)
    ▼
Re-render Component (React)
    ▼
Display Result with Animations
```

---

## 📁 Project Structure

```
frontend/
├── src/
│   ├── App.jsx                  # Main app component & routing
│   ├── main.jsx                 # React entry point
│   ├── index.css                # Global styles
│   │
│   ├── components/
│   │   ├── ChatWindow.jsx       # Q&A chat interface
│   │   ├── Message.jsx          # Chat message bubble
│   │   ├── PolicyEvaluator.jsx  # Policy analysis interface
│   │   ├── SourcesPanel.jsx     # Source citations display
│   │   └── Sidebar.jsx          # Navigation sidebar
│   │
│   └── config/
│       └── api.js               # API client with environment config
│
├── public/
│   └── favicon.svg              # Favicon
│
├── .env.example                 # Environment template
├── package.json                 # Dependencies
├── vite.config.js               # Vite configuration
├── tailwind.config.js           # Tailwind CSS configuration
├── postcss.config.js            # PostCSS configuration
├── index.html                   # HTML entry point
└── README.md                    # This file
```

---

## 🎨 Components

### 1. App.jsx - Main Container

**Purpose**: Root component, mode switching, layout management

**Key Features**:
- Two-mode UI: Chat & Evaluator
- Responsive layout with sidebar
- Dark theme with gradient backgrounds
- Mode persistence (optional)

**Usage**:
```jsx
<App />  // Entry point of the application
```

### 2. ChatWindow.jsx - Q&A Interface

**Purpose**: Real-time chat interface with streaming responses

**Props**: None (uses context/state)

**State**:
```javascript
messages: [
  { type: 'assistant', content: '...', sources: [] },
  { type: 'user', content: '...' }
]
input: string
loading: boolean
includeWebSearch: boolean
currentSources: array
```

**Key Features**:
- Real-time message streaming
- Toggle web search on/off
- Auto-scroll to latest message
- Loading animation while waiting
- Source citations below messages
- Message fade-in animation

**API Call**:
```javascript
const response = await apiClient.chat(userMessage, includeWebSearch)
// Stream: {"type":"content","data":"..."} or {"type":"sources","data":[...]}
```

**Example Message Format**:
```javascript
{
  type: 'assistant',
  content: 'Pakistan education policy focuses on...',
  sources: [
    { type: 'pdf', metadata: { filename: 'NEP.pdf', page: 5 } },
    { type: 'web', title: 'Education Guide', url: 'https://...' }
  ]
}
```

### 3. Message.jsx - Chat Bubble

**Purpose**: Render individual chat messages

**Props**:
```javascript
{
  type: 'user' | 'assistant',  // Message sender
  content: string              // Message text
}
```

**Styling**:
- User: Right-aligned, blue bubble
- Assistant: Left-aligned, purple/gradient bubble
- Markdown support with line breaks
- Readable typography

**Example**:
```jsx
<Message type="user" content="What is education policy?" />
<Message type="assistant" content="Pakistan's education..." />
```

### 4. PolicyEvaluator.jsx - Analysis Interface

**Purpose**: Submit policies for comprehensive evaluation

**State**:
```javascript
policyText: string           // User's policy proposal
loading: boolean             // Processing state
evaluation: string           // LLM evaluation response
sources: array               // Retrieved sources
error: string | null         // Error messages
```

**Key Features**:
- Large textarea for policy input
- Structured evaluation with 5 sections
- Icons for each section (📊 📈 🎯 💪 🚀)
- Parsed sections with better formatting
- Web search indicator
- Sources panel
- Reset button for new evaluation

**Evaluation Sections**:
1. **📊 Comparative Analysis** - vs existing & global policies
2. **📈 Alignment Assessment** - Scores for global/Pakistan context
3. **🎯 Policy Standardization** - Recommended structure
4. **💪 Strengths & Gaps** - Detailed analysis
5. **🚀 Implementation Roadmap** - Phased plan

**Structured Display**:
```javascript
parseEvaluation(text) {
  // Parse ## headings as sections
  // Format content as lists, bold text, paragraphs
  return sections with proper structure
}
```

### 5. SourcesPanel.jsx - Citations

**Purpose**: Display references to sources (PDFs and web)

**Props**:
```javascript
{
  sources: [
    {
      type: 'pdf',
      metadata: { filename: 'policy.pdf', page: 5 }
    },
    {
      type: 'web',
      title: 'Global Best Practices',
      url: 'https://example.com',
      snippet: '...'
    }
  ]
}
```

**Display**:
- PDF sources: Document icon, filename, page number
- Web sources: Link icon, title, clickable URL
- Grid layout on larger screens
- 2-column on desktop, 1-column on mobile

**Example Source Card**:
```javascript
// PDF Source
<div>
  <p className="text-xs font-semibold text-purple-400">📄 PDF Document</p>
  <p className="text-sm text-slate-300">policy.pdf</p>
  <p className="text-xs text-slate-500">Page 5</p>
</div>

// Web Source
<div>
  <p className="text-xs font-semibold text-blue-400">🌐 Web Source</p>
  <p className="text-sm text-slate-300">Global Education Standards</p>
  <a href={url} target="_blank" className="text-xs text-blue-400">View</a>
</div>
```

### 6. Sidebar.jsx - Navigation

**Purpose**: Mode switching and navigation

**Features**:
- Chat mode toggle
- Evaluator mode toggle
- Document list (optional)
- Responsive mobile menu
- Visual mode indicator

---

## 🛠️ Configuration

### Environment Variables

**`.env` file**:
```bash
# Required: API backend URL
VITE_API_URL=http://127.0.0.1:8001

# Optional: Analytics, feature flags, etc.
# VITE_ENABLE_ANALYTICS=true
# VITE_DEBUG=false
```

**Access in Code**:
```javascript
const apiUrl = import.meta.env.VITE_API_URL
// Vite auto-injects as: import.meta.env.VITE_*
```

### Vite Configuration

**vite.config.js**:
```javascript
import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    open: true,  // Auto-open browser
  }
})
```

---

## 🎨 Styling Guide

### Design System

**Color Palette**:
```
Primary:    Purple/Blue (#6366f1, #3b82f6)
Background: Dark Slate (#0f172a, #1e293b, #334155)
Text:       Light Slate (#e2e8f0, #cbd5e1, #94a3b8)
Accent:     Gradient Purple-Blue
```

**Typography**:
```
Headers:    font-bold (text-lg, text-xl)
Body:       font-normal (text-sm, text-base)
Muted:      text-slate-400, text-slate-500
```

**Spacing**:
```
Units: 4px grid (Tailwind default)
Padding: p-4, p-6, p-8
Margin: m-2, m-3, m-4
Gap: gap-2, gap-3, gap-4
```

### Tailwind CSS Configuration

**tailwind.config.js**:
```javascript
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        // Custom colors if needed
      },
      animation: {
        fadeIn: 'fadeIn 0.3s ease-in',
        slideInUp: 'slideInUp 0.4s ease-out'
      }
    }
  },
  plugins: []
}
```

**Custom Animations** (in CSS):
```css
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideInUp {
  from { transform: translateY(20px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}
```

### Component Styling Pattern

**Dark Theme with Gradients**:
```jsx
// Background: Dark gradient
<div className="bg-gradient-to-b from-slate-900 to-slate-950">

// Cards: Glass morphism effect
<div className="bg-slate-800/50 backdrop-blur border border-slate-700/50 rounded-xl">

// Buttons: Gradient with hover effect
<button className="bg-gradient-to-r from-purple-600 to-purple-500 hover:from-purple-700 hover:to-purple-600">

// Text: Gradient text
<h2 className="bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">
```

---

## 🔌 API Integration

### apiClient.js - Configuration

**Purpose**: Centralized API client with environment-based configuration

**Code**:
```javascript
const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8001'

export const apiClient = {
  // Chat endpoint - streaming
  chat: async (question, includeWebSearch = true) => {
    const response = await fetch(`${API_URL}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question, include_web_search: includeWebSearch })
    })
    return response  // Caller handles streaming
  },

  // Evaluation endpoint - returns JSON
  evaluatePolicy: async (policyText) => {
    const response = await fetch(`${API_URL}/evaluate-policy`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ policy_text: policyText })
    })
    return response.json()
  },

  // Health check
  health: async () => {
    const response = await fetch(`${API_URL}/health`)
    return response.json()
  }
}
```

### Streaming Response Handling

**ChatWindow.jsx**:
```javascript
const response = await apiClient.chat(userMessage, includeWebSearch)
const reader = response.body.getReader()
const decoder = new TextDecoder()

while (true) {
  const { done, value } = await reader.read()
  if (done) break
  
  const chunk = decoder.decode(value)
  const lines = chunk.split('\n').filter(line => line.trim())
  
  for (const line of lines) {
    try {
      const json = JSON.parse(line)
      if (json.type === 'content') {
        // Append to message
        assistantContent += json.data
      } else if (json.type === 'sources') {
        // Store sources for display
        sources = json.data
      }
    } catch (e) {
      console.error('Parse error:', e)
    }
  }
}
```

---

## 🚀 Development Workflow

### Hot Module Replacement (HMR)

Vite automatically reloads when you save changes:

```bash
npm run dev
# Edit ChatWindow.jsx and save
# Browser automatically reloads
```

### Debugging

**Browser DevTools** (F12):
- Console: Check for errors
- Network: Monitor API calls
- Performance: Profile rendering
- React DevTools: Inspect component state

**Example Debug Log**:
```javascript
console.log('User message:', userMessage)
console.log('API response:', response)
console.log('Parsed sources:', sources)
```

### Testing Component Locally

```javascript
// Mock data for testing
const mockMessages = [
  { type: 'user', content: 'Test question' },
  { type: 'assistant', content: 'Test answer', sources: [] }
]

// Render with mock data
<ChatWindow messages={mockMessages} />
```

---

## 📦 Dependencies

### Core Dependencies

```json
{
  "react": "^18.2.0",
  "react-dom": "^18.2.0"
}
```

### Build Tools

```json
{
  "vite": "^5.0.0",
  "@vitejs/plugin-react": "^4.0.0"
}
```

### Styling

```json
{
  "tailwindcss": "^3.3.0",
  "postcss": "^8.4.31"
}
```

### HTTP & Networking

```json
{
  "axios": "^1.6.0"  // Optional: if not using fetch
}
```

---

## 📱 Responsive Design

### Breakpoints

Tailwind's default breakpoints:
```
sm: 640px   - Tablets
md: 768px   - Small laptops
lg: 1024px  - Desktops
xl: 1280px  - Large desktops
```

### Responsive Classes

```jsx
// Stack on mobile, row on desktop
<div className="flex flex-col md:flex-row gap-4">

// Hide on mobile, show on desktop
<div className="hidden md:block">

// Responsive font sizes
<h1 className="text-2xl md:text-4xl">

// Responsive padding
<div className="p-4 md:p-8">
```

---

## 🔐 Security Best Practices

### Avoid Sensitive Data

```javascript
// ✅ Correct: Use environment variables
const API_URL = import.meta.env.VITE_API_URL

// ❌ Wrong: Hardcoding URLs
const API_URL = 'https://secret-api.com'
```

### XSS Prevention

```javascript
// ✅ Correct: React auto-escapes by default
<p>{userContent}</p>

// ❌ Wrong: Only for trusted HTML
<p dangerouslySetInnerHTML={{__html: userContent}} />
```

### External Links

```javascript
// ✅ Always open in new tab and verify domain
<a href={source.url} target="_blank" rel="noopener noreferrer">
  View
</a>
```

---

## 📈 Performance Tips

### Code Splitting

```javascript
import { lazy, Suspense } from 'react'

const PolicyEvaluator = lazy(() => import('./PolicyEvaluator'))

<Suspense fallback={<Loading />}>
  <PolicyEvaluator />
</Suspense>
```

### Memoization

```javascript
import { memo } from 'react'

const Message = memo(({ type, content }) => {
  return <div>{content}</div>
})
```

### Image Optimization

```jsx
// Use WebP with fallback
<picture>
  <source srcSet="image.webp" type="image/webp" />
  <img src="image.png" alt="description" />
</picture>
```

---

## 🐛 Common Issues & Solutions

### Issue: CORS Error

**Symptom**:
```
Access to XMLHttpRequest blocked by CORS policy
```

**Solution**:
- Check backend CORS configuration
- Verify VITE_API_URL matches backend
- Backend should allow frontend origin

### Issue: Blank Page

**Symptoms**:
- White screen, no errors

**Solutions**:
```bash
# Clear node_modules and reinstall
rm -rf node_modules
npm install
npm run dev

# Clear browser cache
# Hard refresh: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)
```

### Issue: Hot Reload Not Working

**Symptoms**:
- Changes don't reload automatically

**Solutions**:
```bash
# Restart dev server
npm run dev

# Check vite.config.js has HMR configured
# Delete .vite/ cache and restart
```

---

## 📚 Learning Resources

- **React Docs**: https://react.dev/
- **Vite Docs**: https://vitejs.dev/
- **Tailwind CSS**: https://tailwindcss.com/
- **JavaScript Fetch API**: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API

---

## 🤝 Contributing

When contributing to the frontend:

1. Follow React best practices
2. Use functional components with hooks
3. Keep components focused and reusable
4. Add comments for complex logic
5. Test in multiple screen sizes
6. Ensure accessibility (alt text, labels, etc.)

---

## 📝 License

This frontend is part of the AI Policy Analyzer project, licensed under MIT.

---

<div align="center">

**Built with ❤️ for beautiful policy analysis UIs**

Need help? Check the main [README](../README.md) or [Backend README](../backend/README.md)

</div>
