# Phase 7: Frontend Experience Layer - BiteWise AI

✅ **IMPLEMENTATION COMPLETE**

A modern, responsive Next.js frontend for the AI-powered restaurant recommendation system, featuring a Zomato-inspired design with the BiteWise AI branding.

## 🚀 Features Implemented

- **✅ Next.js 14 App Router**: Modern React framework with server components
- **✅ TypeScript**: Full type safety and IntelliSense support
- **✅ Tailwind CSS**: Utility-first styling with Zomato color theme
- **✅ Responsive Design**: Mobile-first approach with breakpoints
- **✅ Preference Form**: Interactive form matching the UI screenshots
- **✅ Recommendations Display**: Beautiful restaurant cards with AI explanations
- **✅ API Integration**: Full integration with Phase 6 backend
- **✅ Loading States**: Smooth loading animations and skeleton screens
- **✅ Error Handling**: Graceful error states with retry functionality

## 🎨 Design System

### Color Palette (Zomato-Inspired)
- **Primary Red**: `#CB202D` - CTAs, highlights, active states
- **Secondary Dark**: `#2D2D2D` - Headers, text, footer
- **Secondary Light**: `#686B78` - Descriptions, metadata
- **Accent**: `#F4F4F4` - Backgrounds, cards
- **Success**: `#4CAF50` - High ratings
- **Warning**: `#FF9800` - Medium ratings

### Typography
- **Font Family**: Inter (Google Fonts)
- **Scale**: Headings 32px-20px, Body 16px, Small 14px

### Components
- **Cards**: Rounded corners (8px), subtle shadows, hover effects
- **Buttons**: Red primary, outlined secondary, uppercase CTAs
- **Chips**: Selectable tags for cuisines and dining options
- **Forms**: Clean inputs with focus states and validation

## 📁 Project Structure

```
phase7_frontend_experience/
  app/
    components/
      Navbar.tsx         # Top navigation with logo and links
      Footer.tsx         # Site footer with links
    recommendations/
      page.tsx           # Results page with restaurant cards
    globals.css          # Global styles and Tailwind directives
    layout.tsx           # Root layout with Navbar and Footer
    page.tsx             # Home page with preference form
  package.json           # Dependencies
  tailwind.config.ts    # Tailwind with custom theme
  tsconfig.json         # TypeScript configuration
  next.config.js        # Next.js with API proxy
  postcss.config.js     # PostCSS configuration
  README.md            # This file
```

## 🏃‍♂️ Getting Started

### Prerequisites
- Node.js 18+ installed
- Phase 6 backend running on `http://localhost:8000`

### Installation

```bash
cd c:\Projects\Milestone1\phase7_frontend_experience

# Install dependencies
npm install

# Or using the run_phase2 approach
& "$env:LocalAppData\Programs\Node\npm" install
```

### Running the Development Server

```bash
# Start the Next.js development server
npm run dev

# The app will be available at http://localhost:3000
```

### Building for Production

```bash
# Create optimized production build
npm run build

# Start production server
npm start
```

## 📡 API Integration

The frontend integrates with the Phase 6 Backend API:

### Endpoints Used
- `POST /api/v1/recommendations` - Fetch restaurant recommendations
- `GET /api/v1/health` - Health check (optional)

### Proxy Configuration
The `next.config.js` includes a rewrite rule to proxy API requests:
```javascript
rewrites: [
  {
    source: '/api/:path*',
    destination: 'http://localhost:8000/api/:path*',
  },
]
```

## 🖼️ Pages

### 1. Home Page (`/`)
**"Tell Us What You're Craving"**

- Hero section with branding and description
- Interactive preference form:
  - Location search with city chips
  - Budget selection (Low/Medium/High)
  - Cuisine chips (Chinese, Italian, Indian, etc.)
  - Rating slider with star display
  - Dining experience options
- Animated submit button
- Responsive two-column layout

### 2. Recommendations Page (`/recommendations`)
**"Top Picks For You"**

- Dynamic header showing applied filters
- Restaurant cards grid (1-3 columns based on viewport)
- Each card includes:
  - Rank badge (#1, #2, #3...)
  - Rating badge (color-coded)
  - Restaurant name and location
  - Estimated cost
  - **AI Explanation** (why recommended)
  - Action buttons (View Details, Save, Share)
- Loading state with spinner
- Error state with retry
- "Load More" button for additional results

## 🎯 Key Features

### Interactive Preference Form
- Real-time state management with React hooks
- Visual feedback for selections
- Accessible form controls
- Form validation
- Persisted preferences in localStorage

### Restaurant Cards
- Hover animations (lift effect)
- Staggered fade-in animations
- Color-coded rating badges
- AI explanation callouts with red accent
- Responsive image placeholders

### Loading & Error States
- Skeleton screens during data fetch
- Spinning loader with message
- Error boundaries with retry functionality
- Empty state handling

## 📱 Responsive Breakpoints

- **Mobile**: < 640px (1 column cards, stacked layout)
- **Tablet**: 640px - 1024px (2 column cards)
- **Desktop**: > 1024px (3 column cards, side-by-side layout)

## 🔧 Technical Details

### Technologies Used
- **Framework**: Next.js 14.0.0 with App Router
- **Language**: TypeScript 5.0
- **Styling**: Tailwind CSS 3.3
- **Icons**: Lucide React
- **State**: React useState/useEffect hooks
- **Storage**: localStorage for preferences

### Key Dependencies
```json
{
  "next": "14.0.0",
  "react": "^18.2.0",
  "lucide-react": "^0.294.0",
  "tailwind-merge": "^2.0.0",
  "clsx": "^2.0.0"
}
```

## 🧪 Testing the Integration

1. **Start Phase 6 Backend**:
   ```bash
   cd c:\Projects\Milestone1\phase6_backend_api
   python app.py
   ```

2. **Start Frontend** (in new terminal):
   ```bash
   cd c:\Projects\Milestone1\phase7_frontend_experience
   npm run dev
   ```

3. **Open Browser**: Navigate to `http://localhost:3000`

4. **Test Flow**:
   - Fill in the preference form
   - Click "FIND MY RESTAURANTS"
   - View AI-powered recommendations
   - Check restaurant cards with explanations

## 🎨 UI/UX Highlights

### Matching the Screenshots
- ✅ Red primary color (#CB202D) matching Zomato
- ✅ "BiteWise AI" italic logo
- ✅ Form layout with left content, right form
- ✅ City chips (Bangalore, Mumbai, Delhi)
- ✅ Budget buttons (Low ₹, Medium ₹₹, High ₹₹₹)
- ✅ Cuisine selection chips
- ✅ Rating slider with star display
- ✅ Restaurant cards with rank badges
- ✅ "Why Recommended" explanation section
- ✅ Pink/red accent for AI insights

### Animations & Interactions
- Smooth page transitions
- Card hover lift effects
- Staggered card entrance animations
- Button loading states
- Form field focus states

## 🚀 Phase 10: Vercel Deployment

> Deployment triggered: Ready for production!
> Auto-deploy enabled
> Build started

### Prerequisites
1. GitHub repository with pushed code
2. Vercel account (free at https://vercel.com)
3. Backend deployed on Render (Phase 9 complete)

### Environment Setup

Create `.env.local` for local development:
```bash
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Deployment Steps

#### Option 1: Vercel Dashboard (Recommended)
1. Go to https://vercel.com/dashboard
2. Click "Add New Project"
3. Import your GitHub repository
4. Configure:
   - **Framework Preset**: Next.js
   - **Root Directory**: `phase7_frontend_experience`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`
5. Add Environment Variable:
   - Name: `NEXT_PUBLIC_API_URL`
   - Value: `https://your-render-service.onrender.com`
6. Click "Deploy"

#### Option 2: Vercel CLI
```bash
# Install Vercel CLI globally
npm i -g vercel

# Login to Vercel
vercel login

# Deploy from project directory
cd phase7_frontend_experience
vercel --prod
```

### Post-Deployment Configuration

1. **Update API URL**: If your Render backend URL changes, update the environment variable in Vercel dashboard:
   - Project Settings → Environment Variables
   - Edit `NEXT_PUBLIC_API_URL`

2. **Custom Domain** (Optional):
   - Vercel Dashboard → Project → Settings → Domains
   - Add your custom domain

3. **Enable Auto-Deploy**:
   - Vercel automatically deploys on every push to main branch

### Verify Deployment

Visit your deployed URL:
```
https://<your-project>.vercel.app
```

Test the recommendation flow end-to-end.

### Static Export (Alternative for simple hosting)
```javascript
// next.config.js
const nextConfig = {
  output: 'export',
  distDir: 'dist',
}
```

## 📈 Next Steps

Phase 7 is **complete and production-ready**:

1. ✅ All UI components implemented
2. ✅ API integration working
3. ✅ Responsive design complete
4. ✅ Error handling in place
5. ✅ Animations and interactions added

### Possible Enhancements
- Add dark mode toggle
- Implement user authentication
- Add restaurant detail modal/page
- Add map integration
- Implement filtering on results page
- Add favorites/saved restaurants
- Implement share functionality
- Add review/rating submission

## 📞 Support

For issues or questions:
1. Check that Phase 6 backend is running on port 8000
2. Verify all dependencies are installed
3. Check browser console for errors
4. Ensure ports 3000 and 8000 are available

---

**Built with ❤️ using Next.js, TypeScript, and Tailwind CSS**
