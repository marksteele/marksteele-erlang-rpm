PWD = $(shell pwd)
PKG_REVISION?="OTP-17.5.6.8"
PKG_VERSION?="17.5.6.8"
PKG_ID = marksteele-erlang-$(PKG_VERSION)
PKG_BUILD = 1

# No hyphens are allowed in the _version field in RPM
PKG_VERSION_NO_H ?= $(shell echo $(PKG_VERSION) | tr - .)

default:
	#yum-builddep erlang.spec -y
	#rm -rf package/otp
	#mkdir -p package/otp
	#cd package; git clone https://github.com/erlang/otp
	#cd package/otp; git checkout $(PKG_REVISION)
	#rm -rf $(PKG_ID)/
	#GIT_DIR=package/otp/.git git archive --format=tar --prefix=$(PKG_ID)/ $(PKG_REVISION) | tar -xvf -
	#tar -czf $(PKG_ID).tar.gz $(PKG_ID)
	#mkdir -p BUILD packages
	rpmbuild --sign --define "_rpmfilename %%{NAME}-%%{VERSION}-%%{RELEASE}.%%{ARCH}.rpm" \
	--define '_topdir $(PWD)' \
	--define '_sourcedir $(PWD)' \
	--define '_specdir $(PWD)' \
	--define '_rpmdir $(PWD)/packages' \
	--define '_srcrpmdir $(PWD)/packages' \
	--define "_revision $(PKG_VERSION)" \
	--define "_version $(PKG_VERSION_NO_H)" \
	--define "_release $(PKG_BUILD)" \
	--define "_tarname $(PKG_ID).tar.gz" \
	--define "_tarname_base $(PKG_ID)" \
	-ba $(PWD)/erlang.spec
