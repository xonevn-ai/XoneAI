class Xoneai < Formula
    include Language::Python::Virtualenv
  
    desc "AI tools for various AI applications"
    homepage "https://github.com/xonevn-ai/XoneAI"
    url "https://github.com/xonevn-ai/XoneAI/archive/refs/tags/v4.5.15.tar.gz"
    sha256 `curl -sL https://github.com/xonevn-ai/XoneAI/archive/refs/tags/v4.5.15.tar.gz | shasum -a 256`.split.first
    license "MIT"
  
    depends_on "python@3.11"
  
    def install
      virtualenv_install_with_resources
    end
  
    test do
      system "#{bin}/xoneai", "--version"
    end
  end
  