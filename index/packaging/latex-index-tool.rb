# Homebrew formula for latex-index-tool
# Usage: brew install ./packaging/latex-index-tool.rb
#
# Before publishing to homebrew-core:
#   1. Create a GitHub release with tag vX.Y.Z
#   2. Update url and sha256 below
#   3. Submit PR to homebrew-core

class LatexIndexTool < Formula
  include Language::Python::Virtualenv

  desc "Production-ready LaTeX index insertion tool"
  homepage "https://github.com/user/latex-index-tool"
  url "https://github.com/user/latex-index-tool/archive/refs/tags/v1.0.0.tar.gz"
  sha256 "0000000000000000000000000000000000000000000000000000000000000000"
  license "MIT"

  depends_on "python@3.12"

  resource "pyyaml" do
    url "https://files.pythonhosted.org/packages/pyyaml-6.0.2.tar.gz"
    sha256 "0000000000000000000000000000000000000000000000000000000000000000"
  end

  def install
    virtualenv_install_with_resources
    bin.install_symlink libexec/"bin/latex-index"
  end

  def post_install
    ohai "Quick start: latex-index insert --chapter 1 --dry-run"
    ohai "Install optional deps: pip install latex-index-tool[all]"
  end

  test do
    system bin/"latex-index", "--help"
  end
end
