"""
GLITCH MOBILE DEVELOPER AGENT
iOS, Android, and cross-platform specialist
"""

from app.agents.base_agent import BaseAgent
from typing import Dict, Any


class MobileDevAgent(BaseAgent):
    """
    Mobile Developer Agent - builds native and
    cross-platform mobile applications.
    """

    def _get_system_prompt(self) -> str:
        return """You are a Senior Mobile Developer for GLITCH.

Your expertise includes:
- Cross-Platform: React Native, Flutter, Expo
- iOS: Swift, SwiftUI, UIKit
- Android: Kotlin, Jetpack Compose
- State: Redux, MobX, Riverpod
- Navigation: React Navigation, Go Router
- APIs: REST, GraphQL, WebSocket
- Storage: AsyncStorage, SQLite, Realm
- Push: Firebase, OneSignal, APNs

You build:
1. Cross-platform mobile apps
2. Native iOS applications
3. Native Android applications
4. Offline-first experiences
5. Push notification systems
6. Deep linking

Best practices:
- Platform-specific UI patterns
- Offline support
- Performance optimization
- Accessibility
- App store guidelines"""

    async def _process_task(self, task: Dict) -> Dict[str, Any]:
        context = task.get("context", {})

        prompt = f"""
Build mobile application for:

Project: {context.get('project_type', 'mobile app')}
Features: {context.get('features', [])}
Platform: Cross-platform (React Native/Expo)

Generate:
1. App structure and navigation
2. Screen components
3. API integration
4. State management
5. Styling (NativeWind)
"""

        response = await self.llm.generate(prompt, self.system_prompt)
        return self._parse_response(response, "mobile")
