class GitHubUser {
  final String login;
  final String avatarUrl;
  final String? name;
  final String? bio;
  final String? company;
  final String? location;
  final int publicRepos;
  final int followers;
  final int following;
  final String profileUrl;

  const GitHubUser({
    required this.login,
    required this.avatarUrl,
    this.name,
    this.bio,
    this.company,
    this.location,
    required this.publicRepos,
    required this.followers,
    required this.following,
    required this.profileUrl,
  });

  factory GitHubUser.fromJson(Map<String, dynamic> j) => GitHubUser(
        login: j['login'] as String,
        avatarUrl: j['avatar_url'] as String,
        name: j['name'] as String?,
        bio: j['bio'] as String?,
        company: j['company'] as String?,
        location: j['location'] as String?,
        publicRepos: j['public_repos'] as int,
        followers: j['followers'] as int,
        following: j['following'] as int,
        profileUrl: j['html_url'] as String,
      );
}
