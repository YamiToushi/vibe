import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'package:url_launcher/url_launcher.dart';
import '../models/repo.dart';
import '../utils/language_colors.dart';

class RepoCard extends StatefulWidget {
  const RepoCard({super.key, required this.repo});
  final Repo repo;

  @override
  State<RepoCard> createState() => _RepoCardState();
}

class _RepoCardState extends State<RepoCard> {
  bool _hovered = false;

  @override
  Widget build(BuildContext context) {
    final repo = widget.repo;
    final color = langColor(repo.language);
    final created = DateFormat('MMM d, yyyy').format(repo.createdAt);

    return MouseRegion(
      onEnter: (_) => setState(() => _hovered = true),
      onExit: (_) => setState(() => _hovered = false),
      cursor: SystemMouseCursors.click,
      child: GestureDetector(
        onTap: () => launchUrl(Uri.parse(repo.htmlUrl)),
        child: AnimatedContainer(
          duration: const Duration(milliseconds: 180),
          margin: const EdgeInsets.only(bottom: 12),
          decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.circular(12),
            border: Border.all(
              color: _hovered ? color : const Color(0xFFD0D7DE),
              width: _hovered ? 1.5 : 1,
            ),
            boxShadow: [
              BoxShadow(
                color: _hovered
                    ? color.withValues(alpha: 0.15)
                    : Colors.black.withValues(alpha: 0.06),
                blurRadius: _hovered ? 16 : 6,
                offset: const Offset(0, 2),
              ),
            ],
          ),
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // ── Header ────────────────────────────────────────────────
                Row(
                  children: [
                    const Icon(Icons.book_outlined,
                        size: 16, color: Color(0xFF57606A)),
                    const SizedBox(width: 6),
                    Expanded(
                      child: Text(
                        repo.name,
                        style: const TextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.w700,
                          color: Color(0xFF0969DA),
                          letterSpacing: -0.3,
                        ),
                        overflow: TextOverflow.ellipsis,
                      ),
                    ),
                    if (repo.isFork) ...[
                      const SizedBox(width: 8),
                      RepoChip(label: 'Fork', color: const Color(0xFF57606A)),
                    ],
                  ],
                ),

                // ── Description ───────────────────────────────────────────
                if (repo.description != null && repo.description!.isNotEmpty)
                  Padding(
                    padding: const EdgeInsets.only(top: 8),
                    child: Text(
                      repo.description!,
                      style: const TextStyle(
                        fontSize: 13.5,
                        color: Color(0xFF57606A),
                        height: 1.45,
                      ),
                      maxLines: 3,
                      overflow: TextOverflow.ellipsis,
                    ),
                  ),

                // ── Topics ────────────────────────────────────────────────
                if (repo.topics.isNotEmpty)
                  Padding(
                    padding: const EdgeInsets.only(top: 10),
                    child: Wrap(
                      spacing: 6,
                      runSpacing: 4,
                      children: repo.topics
                          .take(5)
                          .map((t) => RepoChip(
                                label: t,
                                color: const Color(0xFF0969DA),
                                background: const Color(0xFFDDF4FF),
                              ))
                          .toList(),
                    ),
                  ),

                const SizedBox(height: 12),
                const Divider(height: 1, color: Color(0xFFF0F0F0)),
                const SizedBox(height: 10),

                // ── Footer meta ───────────────────────────────────────────
                Wrap(
                  spacing: 16,
                  runSpacing: 6,
                  children: [
                    if (repo.language != null)
                      RepoMeta(
                        icon: Icons.circle,
                        iconColor: color,
                        iconSize: 10,
                        label: repo.language!,
                      ),
                    RepoMeta(icon: Icons.star_border_rounded,
                        label: repo.stars.toString()),
                    RepoMeta(icon: Icons.fork_right_rounded,
                        label: repo.forks.toString()),
                    RepoMeta(icon: Icons.calendar_today_outlined,
                        label: created),
                  ],
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

// ── Shared small widgets ──────────────────────────────────────────────────────

class RepoChip extends StatelessWidget {
  const RepoChip({
    super.key,
    required this.label,
    required this.color,
    this.background,
  });
  final String label;
  final Color color;
  final Color? background;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
      decoration: BoxDecoration(
        color: background ?? color.withValues(alpha: 0.1),
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: color.withValues(alpha: 0.3)),
      ),
      child: Text(
        label,
        style: TextStyle(
            fontSize: 11, color: color, fontWeight: FontWeight.w600),
      ),
    );
  }
}

class RepoMeta extends StatelessWidget {
  const RepoMeta({
    super.key,
    required this.icon,
    required this.label,
    this.iconColor,
    this.iconSize,
  });
  final IconData icon;
  final String label;
  final Color? iconColor;
  final double? iconSize;

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        Icon(icon,
            size: iconSize ?? 13,
            color: iconColor ?? const Color(0xFF57606A)),
        const SizedBox(width: 4),
        Text(label,
            style: const TextStyle(fontSize: 12, color: Color(0xFF57606A))),
      ],
    );
  }
}
