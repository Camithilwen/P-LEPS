{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    devenv = {
      url = "github:cachix/devenv";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = {
    self,
    nixpkgs,
    devenv,
    ...
  } @ inputs: {
    devShells = (
      nixpkgs.lib.genAttrs ["x86_64-linux"]
      (system: let
        pkgs = nixpkgs.legacyPackages.${system};
      in {
        default = pkgs.mkShell {
          packages = with pkgs; [
            (python3.withPackages (py:
                with py; [matplotlib pandas tkinter customtkinter scikit-learn tensorflow keras nuitka wheel setuptools cx-freeze]))
          ];
        };

      })
    );
  };
}
