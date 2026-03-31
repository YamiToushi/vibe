import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';
import '../models/repo.dart';
import '../models/github_user.dart';
import '../utils/language_colors.dart';
import '../widgets/repo_card.dart';

class TimelineScreen extends StatefulWidget {
  const TimelineScreen({
    super.key,
    required this.user,
    required this.repos,
  });

  final GitHubUser user;
  final List<Repo> repos;

  @override
  State<TimelineScreen> createState() => _TimelineScreenState();
}

class _TimelineScreenState extends State<TimelineScreen> {
  bool _showForks = false;
  bool _summaryExpanded = true;

  List<Repo> get _filtered => _showForks
      ? widget.repos
      : widget.repos.where((r) => !r.isFork).toList();

  /// Group repos by year, sorted oldest → newest.
  Map<int, List<Repo>> get _byYear {
    final map = <int, List<Repo>>{};
    for (final r in _filtered) {
      map.putIfAbsent(r.createdAt.year, () => []).add(r);
    }
    return Map.fromEntries(
      map.entries.toList()..sort((a, b) => a.key.compareTo(b.key)),
    );
  }

  /// Repos per year for the chart (uses ALL repos, not filtered).
  Map<int, int> get _yearCounts {
    final map = <int, int>{};
    for (final r in widget.repos) {
      map[r.createdAt.year] = (map[r.createdAt.year] ?? 0) + 1;
    }
    return Map.fromEntries(
      map.entries.toList()..sort((a, b) => a.key.compareTo(b.key)),
    );
  }

  @override
  Widget build(BuildContext context) {
    final byYear = _byYear;
    final user = widget.user;

    return Scaffold(
      backgroundColor: const Color(0xFFF6F8FA),
      appBar: _buildAppBar(user),
      body: CustomScrollView(
        slivers: [
          // ── Profile header ─────────────────────────────────────────────
          SliverToBoxAdapter(child: _ProfileCard(user: user)),

          // ── Bonus: Year summary chart ──────────────────────────────────
          SliverToBoxAdapter(
            child: _YearSummaryCard(
              yearCounts: _yearCounts,
              expanded: _summaryExpanded,
              onToggle: () =>
                  setState(() => _summaryExpanded = !_summaryExpanded),
            ),
          ),

          // ── Fork toggle ────────────────────────────────────────────────
          SliverToBoxAdapter(
            child: Padding(
              padding:
                  const EdgeInsets.symmetric(horizontal: 20, vertical: 4),
              child: Row(
                children: [
                  Text(
                    '${_filtered.length} repositories',
                    style: const TextStyle(
                      fontSize: 13,
                      color: Color(0xFF57606A),
                      fontWeight: FontWeight.w500,
                    ),
                  ),
                  const Spacer(),
                  const Text('Show forks',
                      style: TextStyle(
                          fontSize: 13, color: Color(0xFF57606A))),
                  const SizedBox(width: 6),
                  Switch.adaptive(
                    value: _showForks,
                    onChanged: (v) => setState(() => _showForks = v),
                    activeThumbColor: const Color(0xFF0969DA),
                    activeTrackColor:
                        const Color(0xFF0969DA).withValues(alpha: 0.4),
                  ),
                ],
              ),
            ),
          ),

          // ── Timeline ───────────────────────────────────────────────────
          if (byYear.isEmpty)
            const SliverFillRemaining(
              child: Center(
                child: Text('No repositories to display.',
                    style: TextStyle(color: Color(0xFF57606A))),
              ),
            )
          else
            SliverPadding(
              padding: const EdgeInsets.fromLTRB(20, 8, 20, 40),
              sliver: SliverList(
                delegate: SliverChildBuilderDelegate(
                  (context, index) {
                    final year = byYear.keys.elementAt(index);
                    final repos = byYear[year]!;
                    return _YearSection(year: year, repos: repos);
                  },
                  childCount: byYear.length,
                ),
              ),
            ),
        ],
      ),
    );
  }

  AppBar _buildAppBar(GitHubUser user) {
    return AppBar(
      backgroundColor: const Color(0xFF24292F),
      foregroundColor: Colors.white,
      elevation: 0,
      title: Row(
        children: [
          CircleAvatar(
            radius: 14,
            backgroundImage: NetworkImage(user.avatarUrl),
          ),
          const SizedBox(width: 10),
          Text(
            user.login,
            style: const TextStyle(
                fontSize: 16, fontWeight: FontWeight.w700),
          ),
          const SizedBox(width: 8),
          Container(
            padding:
                const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
            decoration: BoxDecoration(
              color: Colors.white.withValues(alpha: 0.15),
              borderRadius: BorderRadius.circular(20),
            ),
            child: Text(
              '${widget.repos.length} repos',
              style: const TextStyle(fontSize: 11),
            ),
          ),
        ],
      ),
      actions: [
        IconButton(
          icon: const Icon(Icons.open_in_new_rounded, size: 20),
          tooltip: 'Open GitHub profile',
          onPressed: () => launchUrl(Uri.parse(user.profileUrl)),
        ),
      ],
    );
  }
}

// ── Profile card ──────────────────────────────────────────────────────────────

class _ProfileCard extends StatelessWidget {
  const _ProfileCard({required this.user});
  final GitHubUser user;

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.fromLTRB(20, 16, 20, 8),
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(14),
        border: Border.all(color: const Color(0xFFD0D7DE)),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.05),
            blurRadius: 8,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Avatar
          ClipRRect(
            borderRadius: BorderRadius.circular(50),
            child: Image.network(
              user.avatarUrl,
              width: 64,
              height: 64,
              fit: BoxFit.cover,
              errorBuilder: (_, __, ___) => const CircleAvatar(
                radius: 32,
                backgroundColor: Color(0xFFD0D7DE),
                child: Icon(Icons.person, color: Color(0xFF57606A)),
              ),
            ),
          ),
          const SizedBox(width: 16),

          // Info
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                if (user.name != null && user.name!.isNotEmpty)
                  Text(
                    user.name!,
                    style: const TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.w700,
                      color: Color(0xFF24292F),
                    ),
                  ),
                Text(
                  '@${user.login}',
                  style: const TextStyle(
                    fontSize: 14,
                    color: Color(0xFF57606A),
                  ),
                ),
                if (user.bio != null && user.bio!.isNotEmpty) ...[
                  const SizedBox(height: 6),
                  Text(
                    user.bio!,
                    style: const TextStyle(
                      fontSize: 13,
                      color: Color(0xFF57606A),
                      height: 1.4,
                    ),
                    maxLines: 2,
                    overflow: TextOverflow.ellipsis,
                  ),
                ],
                const SizedBox(height: 10),
                Wrap(
                  spacing: 16,
                  children: [
                    RepoMeta(
                      icon: Icons.people_outline,
                      label: '${user.followers} followers',
                    ),
                    RepoMeta(
                      icon: Icons.book_outlined,
                      label: '${user.publicRepos} public repos',
                    ),
                    if (user.location != null)
                      RepoMeta(
                        icon: Icons.location_on_outlined,
                        label: user.location!,
                      ),
                  ],
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

// ── Year summary chart (bonus) ────────────────────────────────────────────────

class _YearSummaryCard extends StatelessWidget {
  const _YearSummaryCard({
    required this.yearCounts,
    required this.expanded,
    required this.onToggle,
  });

  final Map<int, int> yearCounts;
  final bool expanded;
  final VoidCallback onToggle;

  @override
  Widget build(BuildContext context) {
    final maxCount =
        yearCounts.values.fold(0, (a, b) => a > b ? a : b);
    final total =
        yearCounts.values.fold(0, (a, b) => a + b);

    return Container(
      margin: const EdgeInsets.fromLTRB(20, 8, 20, 8),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(14),
        border: Border.all(color: const Color(0xFFD0D7DE)),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.04),
            blurRadius: 8,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Column(
        children: [
          // ── Header ──────────────────────────────────────────────────────
          InkWell(
            onTap: onToggle,
            borderRadius: BorderRadius.circular(14),
            child: Padding(
              padding: const EdgeInsets.fromLTRB(16, 14, 16, 14),
              child: Row(
                children: [
                  const Icon(Icons.bar_chart_rounded,
                      size: 18, color: Color(0xFF0969DA)),
                  const SizedBox(width: 8),
                  const Text(
                    'Repositories by Year',
                    style: TextStyle(
                      fontSize: 14,
                      fontWeight: FontWeight.w700,
                      color: Color(0xFF24292F),
                    ),
                  ),
                  const SizedBox(width: 8),
                  Container(
                    padding: const EdgeInsets.symmetric(
                        horizontal: 8, vertical: 2),
                    decoration: BoxDecoration(
                      color: const Color(0xFFDDF4FF),
                      borderRadius: BorderRadius.circular(20),
                    ),
                    child: Text(
                      '$total total',
                      style: const TextStyle(
                        fontSize: 11,
                        color: Color(0xFF0969DA),
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                  ),
                  const Spacer(),
                  Icon(
                    expanded
                        ? Icons.keyboard_arrow_up_rounded
                        : Icons.keyboard_arrow_down_rounded,
                    color: const Color(0xFF57606A),
                  ),
                ],
              ),
            ),
          ),

          // ── Chart ────────────────────────────────────────────────────────
          AnimatedCrossFade(
            duration: const Duration(milliseconds: 220),
            crossFadeState: expanded
                ? CrossFadeState.showFirst
                : CrossFadeState.showSecond,
            firstChild: Padding(
              padding: const EdgeInsets.fromLTRB(16, 0, 16, 16),
              child: Column(
                children: yearCounts.entries.map((e) {
                  final year = e.key;
                  final count = e.value;
                  final fraction = maxCount > 0 ? count / maxCount : 0.0;
                  final color = yearColor(year);

                  return Padding(
                    padding: const EdgeInsets.symmetric(vertical: 4),
                    child: Row(
                      children: [
                        SizedBox(
                          width: 44,
                          child: Text(
                            '$year',
                            style: const TextStyle(
                              fontSize: 12,
                              fontWeight: FontWeight.w600,
                              color: Color(0xFF57606A),
                            ),
                          ),
                        ),
                        Expanded(
                          child: LayoutBuilder(
                            builder: (context, constraints) {
                              return Stack(
                                children: [
                                  Container(
                                    height: 20,
                                    decoration: BoxDecoration(
                                      color:
                                          const Color(0xFFF0F0F0),
                                      borderRadius:
                                          BorderRadius.circular(4),
                                    ),
                                  ),
                                  AnimatedContainer(
                                    duration: const Duration(
                                        milliseconds: 600),
                                    curve: Curves.easeOutCubic,
                                    height: 20,
                                    width: constraints.maxWidth *
                                        fraction,
                                    decoration: BoxDecoration(
                                      color: color,
                                      borderRadius:
                                          BorderRadius.circular(4),
                                    ),
                                  ),
                                ],
                              );
                            },
                          ),
                        ),
                        const SizedBox(width: 8),
                        SizedBox(
                          width: 28,
                          child: Text(
                            '$count',
                            style: TextStyle(
                              fontSize: 12,
                              fontWeight: FontWeight.w700,
                              color: color,
                            ),
                          ),
                        ),
                      ],
                    ),
                  );
                }).toList(),
              ),
            ),
            secondChild: const SizedBox.shrink(),
          ),
        ],
      ),
    );
  }
}

// ── Year section with timeline line ──────────────────────────────────────────

class _YearSection extends StatelessWidget {
  const _YearSection({required this.year, required this.repos});
  final int year;
  final List<Repo> repos;

  @override
  Widget build(BuildContext context) {
    final color = yearColor(year);

    return IntrinsicHeight(
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          // ── Timeline spine ───────────────────────────────────────────
          SizedBox(
            width: 52,
            child: Column(
              children: [
                // Year badge
                Container(
                  width: 48,
                  padding: const EdgeInsets.symmetric(vertical: 5),
                  decoration: BoxDecoration(
                    color: color,
                    borderRadius: BorderRadius.circular(24),
                    boxShadow: [
                      BoxShadow(
                        color: color.withValues(alpha: 0.35),
                        blurRadius: 8,
                        offset: const Offset(0, 2),
                      ),
                    ],
                  ),
                  child: Text(
                    '$year',
                    textAlign: TextAlign.center,
                    style: const TextStyle(
                      fontSize: 12,
                      fontWeight: FontWeight.w800,
                      color: Colors.white,
                      letterSpacing: 0.3,
                    ),
                  ),
                ),
                // Vertical line
                Expanded(
                  child: Center(
                    child: Container(
                      width: 2,
                      color: color.withValues(alpha: 0.25),
                    ),
                  ),
                ),
              ],
            ),
          ),

          const SizedBox(width: 12),

          // ── Repo cards ───────────────────────────────────────────────
          Expanded(
            child: Padding(
              padding: const EdgeInsets.only(top: 4, bottom: 16),
              child: Column(
                children: repos
                    .map((r) => RepoCard(repo: r))
                    .toList(),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
