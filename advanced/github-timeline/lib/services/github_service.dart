import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/repo.dart';
import '../models/github_user.dart';

// ── Custom exceptions ─────────────────────────────────────────────────────────

class GitHubUserNotFoundException implements Exception {
  final String username;
  const GitHubUserNotFoundException(this.username);
  @override
  String toString() => 'User "$username" was not found on GitHub.';
}

class GitHubRateLimitException implements Exception {
  @override
  String toString() =>
      'GitHub API rate limit exceeded. Please wait a minute and try again.';
}

class GitHubApiException implements Exception {
  final String message;
  const GitHubApiException(this.message);
  @override
  String toString() => 'GitHub API error: $message';
}

// ── Service ───────────────────────────────────────────────────────────────────

class GitHubService {
  static const _base = 'https://api.github.com';
  static const _headers = {'Accept': 'application/vnd.github.v3+json'};

  final http.Client _client;
  GitHubService({http.Client? client}) : _client = client ?? http.Client();

  Future<GitHubUser> getUser(String username) async {
    final res = await _client.get(
      Uri.parse('$_base/users/$username'),
      headers: _headers,
    );
    _checkStatus(res, username);
    return GitHubUser.fromJson(json.decode(res.body) as Map<String, dynamic>);
  }

  Future<List<Repo>> getRepos(String username) async {
    final repos = <Repo>[];
    for (var page = 1; ; page++) {
      final res = await _client.get(
        Uri.parse(
          '$_base/users/$username/repos'
          '?sort=created&direction=asc&per_page=100&page=$page',
        ),
        headers: _headers,
      );
      _checkStatus(res, username);
      final data = json.decode(res.body) as List<dynamic>;
      repos.addAll(data.map((e) => Repo.fromJson(e as Map<String, dynamic>)));
      if (data.length < 100) break;
    }
    return repos;
  }

  void _checkStatus(http.Response res, String username) {
    switch (res.statusCode) {
      case 200:
        return;
      case 404:
        throw GitHubUserNotFoundException(username);
      case 403:
        throw GitHubRateLimitException();
      default:
        throw GitHubApiException('HTTP ${res.statusCode}');
    }
  }
}
