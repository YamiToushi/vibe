import 'package:flutter/material.dart';
import '../models/repo.dart';
import '../models/github_user.dart';
import '../services/github_service.dart';
import 'timeline_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final _controller = TextEditingController();
  final _formKey = GlobalKey<FormState>();
  final _service = GitHubService();

  bool _loading = false;
  String? _error;

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  Future<void> _generate() async {
    if (!(_formKey.currentState?.validate() ?? false)) return;

    final username = _controller.text.trim();
    setState(() {
      _loading = true;
      _error = null;
    });

    try {
      final results = await Future.wait([
        _service.getUser(username),
        _service.getRepos(username),
      ]);
      if (!mounted) return;

      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (_) => TimelineScreen(
            user: results[0] as GitHubUser,
            repos: results[1] as List<Repo>,
          ),
        ),
      );
    } on GitHubUserNotFoundException catch (e) {
      setState(() => _error = e.toString());
    } on GitHubRateLimitException catch (e) {
      setState(() => _error = e.toString());
    } on GitHubApiException catch (e) {
      setState(() => _error = e.toString());
    } catch (e) {
      setState(() => _error = 'Unexpected error: $e');
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(24),
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 480),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                // ── Logo / Hero ──────────────────────────────────────────
                Container(
                  width: 80,
                  height: 80,
                  decoration: BoxDecoration(
                    color: const Color(0xFF24292F),
                    borderRadius: BorderRadius.circular(20),
                    boxShadow: [
                      BoxShadow(
                        color: Colors.black.withValues(alpha: 0.15),
                        blurRadius: 20,
                        offset: const Offset(0, 6),
                      ),
                    ],
                  ),
                  child: const Icon(Icons.hub_rounded,
                      size: 42, color: Colors.white),
                ),
                const SizedBox(height: 24),
                const Text(
                  'GitHub Timeline',
                  style: TextStyle(
                    fontSize: 30,
                    fontWeight: FontWeight.w800,
                    color: Color(0xFF24292F),
                    letterSpacing: -0.8,
                  ),
                ),
                const SizedBox(height: 8),
                const Text(
                  'Generate a beautiful visual history\nof any GitHub user\'s public repositories.',
                  textAlign: TextAlign.center,
                  style: TextStyle(
                    fontSize: 15,
                    color: Color(0xFF57606A),
                    height: 1.5,
                  ),
                ),
                const SizedBox(height: 40),

                // ── Input card ───────────────────────────────────────────
                Container(
                  padding: const EdgeInsets.all(24),
                  decoration: BoxDecoration(
                    color: Colors.white,
                    borderRadius: BorderRadius.circular(16),
                    border:
                        Border.all(color: const Color(0xFFD0D7DE)),
                    boxShadow: [
                      BoxShadow(
                        color: Colors.black.withValues(alpha: 0.05),
                        blurRadius: 12,
                        offset: const Offset(0, 4),
                      ),
                    ],
                  ),
                  child: Form(
                    key: _formKey,
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.stretch,
                      children: [
                        const Text(
                          'GitHub Username',
                          style: TextStyle(
                            fontSize: 13,
                            fontWeight: FontWeight.w600,
                            color: Color(0xFF24292F),
                          ),
                        ),
                        const SizedBox(height: 8),
                        TextFormField(
                          controller: _controller,
                          autofocus: true,
                          textInputAction: TextInputAction.go,
                          onFieldSubmitted: (_) => _generate(),
                          decoration: const InputDecoration(
                            hintText: 'e.g. torvalds',
                            prefixIcon: Icon(Icons.alternate_email,
                                size: 18, color: Color(0xFF57606A)),
                          ),
                          validator: (v) {
                            if (v == null || v.trim().isEmpty) {
                              return 'Please enter a GitHub username.';
                            }
                            final valid = RegExp(
                                    r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,37}[a-zA-Z0-9])?$')
                                .hasMatch(v.trim());
                            if (!valid) {
                              return 'Not a valid GitHub username format.';
                            }
                            return null;
                          },
                        ),
                        const SizedBox(height: 16),

                        // ── Error banner ─────────────────────────────────
                        if (_error != null) ...[
                          Container(
                            padding: const EdgeInsets.all(12),
                            decoration: BoxDecoration(
                              color: const Color(0xFFFFEBE9),
                              borderRadius: BorderRadius.circular(8),
                              border: Border.all(
                                  color: const Color(0xFFFF818266)),
                            ),
                            child: Row(
                              children: [
                                const Icon(Icons.error_outline,
                                    size: 16,
                                    color: Color(0xFFCF222E)),
                                const SizedBox(width: 8),
                                Expanded(
                                  child: Text(
                                    _error!,
                                    style: const TextStyle(
                                      fontSize: 13,
                                      color: Color(0xFFCF222E),
                                    ),
                                  ),
                                ),
                              ],
                            ),
                          ),
                          const SizedBox(height: 16),
                        ],

                        // ── Generate button ──────────────────────────────
                        SizedBox(
                          height: 46,
                          child: FilledButton.icon(
                            onPressed: _loading ? null : _generate,
                            icon: _loading
                                ? const SizedBox(
                                    width: 16,
                                    height: 16,
                                    child: CircularProgressIndicator(
                                      strokeWidth: 2,
                                      color: Colors.white,
                                    ),
                                  )
                                : const Icon(Icons.auto_awesome,
                                    size: 18),
                            label: Text(
                                _loading ? 'Generating…' : 'Generate Timeline'),
                            style: FilledButton.styleFrom(
                              backgroundColor: const Color(0xFF1A7F37),
                              disabledBackgroundColor:
                                  const Color(0xFF1A7F37).withValues(alpha: 0.6),
                              shape: RoundedRectangleBorder(
                                borderRadius: BorderRadius.circular(8),
                              ),
                              textStyle: const TextStyle(
                                fontSize: 15,
                                fontWeight: FontWeight.w600,
                              ),
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                ),

                const SizedBox(height: 32),
                // ── Footer hint ──────────────────────────────────────────
                Wrap(
                  spacing: 20,
                  children: [
                    _HintChip(icon: Icons.lock_open_outlined,
                        label: 'Public repos only'),
                    _HintChip(icon: Icons.sort_rounded,
                        label: 'Sorted by date'),
                    _HintChip(icon: Icons.bar_chart_rounded,
                        label: 'Year summary'),
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

class _HintChip extends StatelessWidget {
  const _HintChip({required this.icon, required this.label});
  final IconData icon;
  final String label;

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        Icon(icon, size: 14, color: const Color(0xFF57606A)),
        const SizedBox(width: 4),
        Text(label,
            style: const TextStyle(
                fontSize: 12, color: Color(0xFF57606A))),
      ],
    );
  }
}
