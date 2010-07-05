from reviewboard.scmtools.errors import FileNotFoundError, SCMError
        self.client = GitClient(repository.path)

    def _resolve_head(self, revision, path):
        if revision == HEAD:
            if path == "":
                raise SCMError("path must be supplied if revision is %s" % HEAD)
            return "HEAD:%s" % path
        else:
            return revision
        return self.client.cat_file(self._resolve_head(revision, path))
            type = self.client.cat_file(self._resolve_head(revision, path), option="-t")
            return type and type.strip() == "blob"
            (i, file) = self._parse_diff(i)
            if file:
                self.files.append(file)
    def _parse_diff(self, i):
        if self.lines[i].startswith("diff --git"):
            # First check if it is a new file with no content or
            # a file mode change with no content or
            # a deleted file with no content
            # then skip
            try:
                if ((self.lines[i + 1].startswith("new file mode") or
                     self.lines[i + 1].startswith("old mode") or
                     self.lines[i + 1].startswith("deleted file mode")) and
                    self.lines[i + 3].startswith("diff --git")):
                    i += 3
                    return i, None
            except IndexError, x:
                # This means this is the only bit left in the file
                i += 3
                return i, None

            # Now we have a diff we are going to use so get the filenames + commits
            file = File()
            file.data = self.lines[i] + "\n"
            file.binary = False
            diffLine = self.lines[i].split()
            try:
                # Need to remove the "a/" and "b/" prefix
                remPrefix = re.compile("^[a|b]/");
                file.origFile = remPrefix.sub("", diffLine[-2])
                file.newFile = remPrefix.sub("", diffLine[-1])
            except ValueError:
                raise DiffParserError(
                    "The diff file is missing revision information",
                    i)
            i += 1

            # We have no use for recording this info so skip it
            if self.lines[i].startswith("new file mode") \
               or self.lines[i].startswith("deleted file mode"):
                i += 1
            elif self.lines[i].startswith("old mode") \
                 and self.lines[i + 1].startswith("new mode"):
                i += 2

            # Get the revision info
            if i < len(self.lines) and self.lines[i].startswith("index "):
                indexRange = self.lines[i].split(None, 2)[1]
                file.origInfo, file.newInfo = indexRange.split("..")
                if self.pre_creation_regexp.match(file.origInfo):
                    file.origInfo = PRE_CREATION
                i += 1

            # Get the changes
            while i < len(self.lines):
                if self.lines[i].startswith("diff --git"):
                    return i, file

                if self.lines[i].startswith("Binary files") or \
                   self.lines[i].startswith("GIT binary patch"):
                    file.binary = True
                    return i + 1, file

                if i + 1 < len(self.lines) and \
                   (self.lines[i].startswith('--- ') and \
                     self.lines[i + 1].startswith('+++ ')):
                    if self.lines[i].split()[1] == "/dev/null":
                        file.origInfo = PRE_CREATION

                file.data += self.lines[i] + "\n"
                i += 1

            return i, file
        return i + 1, None


class GitClient:
    def __init__(self, path):
        self.path = path
            ['git', '--git-dir=%s' % self.path, 'config',
                 'core.repositoryformatversion'],
            raise ImportError
    def cat_file(self, commit, option="blob"):
            ['git', '--git-dir=%s' % self.path, 'cat-file',
                 '%s' % option, '%s' % commit],