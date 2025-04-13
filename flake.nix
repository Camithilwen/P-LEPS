{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    devenv.url = "github:cachix/devenv";
  };

  outputs = { self, nixpkgs, devenv, ... } @ inputs:
  let
    system = "x86_64-linux";
    pkgs = nixpkgs.legacyPackages.${system};
  in {
    packages.${system} = {
      loan-app = pkgs.stdenv.mkDerivation {
        name = "loan-app";
        src = ./.;
        buildInputs = [
          (pkgs.python3.withPackages (py: [
            py.matplotlib py.pandas py.tkinter py.customtkinter
            py.scikit-learn py.tensorflow py.keras py.nuitka
          ]))
          pkgs.libxcrypt
        ];
        installPhase = ''
          mkdir -p $out/bin
          cp gui_5_0 $out/bin/
        '';
      };

      dockerImage = pkgs.dockerTools.buildImage {
        name = "loan-app";
        tag = "latest";
        contents = [ self.packages.${system}.loan-app pkgs.bashInteractive ];
        config = {
          Cmd = [ "${self.packages.${system}.loan-app}/bin/gui_5_0" ];
          Env = [
            "PYTHONPATH=/app"
            "LD_LIBRARY_PATH=${pkgs.libxcrypt}/lib"
          ];
        };
      };
    };

    devShells.${system}.default = pkgs.mkShell {
      packages = with pkgs; [
        (python3.withPackages (py: [
          py.matplotlib py.pandas py.tkinter py.customtkinter
          py.scikit-learn py.tensorflow py.keras py.nuitka
        ]))
        xorg.xhost
      ];
    };
  };
}
