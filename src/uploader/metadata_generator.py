"""
Metadata Generator Module
Generates SEO-optimized, hook-aligned YouTube Shorts titles, descriptions, hashtags, and tag sets.
Strictly adheres to channel branding guidelines and YouTube packaging principles.
"""

from typing import Dict, Any, List

class MetadataGenerator:
    def __init__(self, channel_name: str = "Jhaji OG", game_title: str = "ScarFall 2.0"):
        self.channel_name = channel_name
        self.game_title = game_title

    def generate_multikill_metadata(self, title_prefix: str, kills_breakdown: List[str]) -> Dict[str, Any]:
        """
        Generates standard metadata package for a multi-kill tournament short.
        """
        title = f"{title_prefix} Tournament Frags | {self.channel_name}, Clutch Shorts #shorts #scarfall2 #gaming"

        breakdown_text = "\n".join([f"{i+1}. {item}" for i, item in enumerate(kills_breakdown)])
        description = (
            f"{title_prefix} Tournament Frags | {self.channel_name}, Clutch Shorts\n\n"
            f"Insane pro tournament frags back-to-back:\n"
            f"{breakdown_text}\n\n"
            f"Subscribe to {self.channel_name} for daily {self.game_title} & BGMI competitive frags, clutches & tournament highlights!\n"
            f"Follow on Kick: https://kick.com/jhajiog\n"
            f"Join Discord: https://discord.gg/uVebERX\n"
            f"ODDSOCEAN Esports Instagram: https://instagram.com/oddsocean.in\n\n"
            f"#shorts #scarfall2 #gaming #clutch #esportsindia #battleroyale #jhajiog #oddsocean #tournamentfrags"
        )

        tags = [
            "scarfall 2.0",
            "scarfall 2.0 clutch",
            "tournament frags",
            "4 kills montage",
            "squad wipe",
            "jhaji og",
            "oddsocean",
            "cloud9",
            "kyzn",
            "esports india",
            "shorts",
            "gaming shorts"
        ]

        return {
            "title": title,
            "description": description,
            "audience": "No, it's not made for kids",
            "tags": ", ".join(tags),
            "visibility": "Scheduled"
        }

if __name__ == "__main__":
    gen = MetadataGenerator()
    data = gen.generate_multikill_metadata(
        title_prefix="4 Kills Multi-Squad Wipe",
        kills_breakdown=[
            "Double Wipe vs Cloud9 Esports (C9x)",
            "80m 6x Scope Laser Spray vs TSF",
            "High Ground Ridge Clash vs KyZN Esports",
            "Final 1v1 Circle Clutch for the Victory!"
        ]
    )
    print("Generated Title:", data["title"])
